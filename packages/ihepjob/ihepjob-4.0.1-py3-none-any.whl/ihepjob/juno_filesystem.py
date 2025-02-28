###############################################################################
# Author: Xuefeng DING <dingxf@ihep.ac.cn> @ IHEP-CAS
#
# Project: B8-analysis
# Date: 2025 February 10th
# Version: v1.0
# Description:
#   eos helper
#
# Maintainer:
#   Xuefeng Ding <dingxf@ihep.ac.cn>
#
# All rights reserved. 2024 copyrighted.
###############################################################################
import os
import re
import shutil
from abc import ABC, abstractmethod
from typing import Optional

from loguru import logger
from XRootD.client import FileSystem as XRootDFileSystem
from XRootD.client.flags import DirListFlags, MkDirFlags, StatInfoFlags


class FileSystem(ABC):
    @abstractmethod
    def exists(self, path: str, min_size=0):
        pass

    @abstractmethod
    def chmod(self, path: str, mode: int):
        pass

    @abstractmethod
    def cp(self, source: str, dest: str, force=False):
        pass

    @abstractmethod
    def rm(self, path: str):
        pass

    @abstractmethod
    def ls(self, path: str, recursive: bool = False):
        pass

    @abstractmethod
    def mkdir(self, path: str, exist_ok: bool = True):
        pass


class EOSFileSystem(FileSystem):
    def __init__(self, server: str = "root://junoeos01.ihep.ac.cn/"):
        self.server = server
        self.fs = XRootDFileSystem(server)

    def exists(self, path: str, min_size: int = 0):
        status, info = self.fs.stat(path)
        return status.ok and info.size >= min_size

    def chmod(self, path: str, mode: int):
        status = self.fs.chmod(path, mode)
        return status.ok

    def cp(self, source: str, dest: str, force: bool = False):
        logger.debug(f"eos cp {source} {dest}")
        if self.exists(dest):
            if force:
                self.rm(dest)
            else:
                logger.warning(f"Destination {dest} exists on EOS, skipping (force=False)")
                return False
        source = source.replace("/eos/", f"{self.server}/eos/")
        dest = dest.replace("/eos/", f"{self.server}/eos/")
        status, _ = self.fs.copy(source, dest)
        if status.ok:
            logger.info(f"Copied {source} to {dest} on EOS")
            return True
        logger.error(f"Copy failed on EOS: {status.message}")
        return False

    def rm(self, path: str):
        status, _ = self.fs.rm(path)
        return status.ok

    def ls(self, path: str, recursive: bool = False, pattern: Optional[str] = None):
        if pattern:
            regex = re.compile(pattern)

        file_list = []
        if not self.exists(path):
            logger.error(f"Path does not exist: {path}")
            return file_list

        def rec_list(directory):
            status, listing = self.fs.dirlist(directory, DirListFlags.STAT)
            if not status.ok:
                logger.error(f"Error listing directory {directory}: {status.message}")
                return file_list
            for entry in listing:
                file_name = entry.name
                full_path = os.path.join(directory.rstrip("/"), file_name)
                if entry.statinfo.flags & StatInfoFlags.IS_DIR:
                    if recursive:
                        rec_list(full_path)
                elif pattern is None or regex.match(file_name):
                    logger.trace(f"found a file matching: {full_path}")
                    file_list.append(full_path)

        rec_list(path)
        logger.debug(f"ls <{path}> regex <{pattern}> found {len(file_list)} files")
        return file_list

    def mkdir(self, path: str, exist_ok: bool = True):
        if self.exists(path):
            status, info = self.fs.stat(path)
            return bool(info.flags & StatInfoFlags.IS_DIR and exist_ok)
        status, _ = self.fs.mkdir(path, mode=0o755, flags=MkDirFlags.MAKEPATH)
        return status.ok


class LocalFileSystem(FileSystem):
    def exists(self, path: str, min_size: int = 0):
        return os.path.exists(path) and os.path.getsize(path) >= min_size

    def chmod(self, path: str, mode: int):
        os.chmod(path, mode)
        return True

    def cp(self, source: str, dest: str, force: bool = False):
        if self.exists(dest):
            if force:
                os.remove(dest)
            else:
                logger.warning(f"Destination {dest} exists locally, skipping (force=False)")
                return False
        shutil.copy(source, dest)
        logger.info(f"Copied {source} to {dest} locally")
        return True

    def rm(self, path: str):
        if os.path.exists(path):
            os.remove(path)
            return True
        return False

    def ls(self, path: str, recursive: bool = False, pattern: Optional[str] = None):
        if pattern:
            regex = re.compile(pattern)

        file_list = []
        if not self.exists(path):
            logger.error(f"Path does not exist: {path}")
            return file_list

        def rec_list(directory):
            try:
                entries = os.listdir(directory)
                for entry in entries:
                    file_name = entry
                    full_path = os.path.join(directory, file_name)
                    logger.debug(f"{full_path} {file_name} {pattern} {regex.match(file_name)}")
                    if os.path.isdir(full_path):
                        if recursive:
                            rec_list(full_path)
                    elif os.path.isfile(full_path) and (pattern is None or regex.match(file_name)):
                        logger.trace(f"found a file matching: {full_path}")
                        file_list.append(full_path)
            except Exception as e:
                logger.error(f"Error listing directory {directory}: {e}")

        rec_list(path)
        logger.debug(f"ls <{path}> regex <{pattern}> found {len(file_list)} files")
        return file_list

    def mkdir(self, path: str, exist_ok: bool = True):
        try:
            os.makedirs(path, mode=0o755, exist_ok=exist_ok)
            return True
        except FileExistsError:
            return False
        except Exception:
            return False


class FileSystemManager:
    def __init__(self, test_mode=False):
        self.local_fs = LocalFileSystem()
        self.eos_fs = EOSFileSystem()
        self.default_fs = self.local_fs if test_mode else self.eos_fs

    def get_fs(self, path: str):
        """Determine the appropriate FileSystem for a given path."""
        if path.startswith("/eos/") or path.startswith("root://"):
            return self.eos_fs
        return self.local_fs

    def dirname(self, path: str) -> str:
        """Extract directory path, handling URI schemes."""
        return "/".join(path.split("/")[:-1]) if "/" in path else ""

    def exists(self, path: str):
        return self.get_fs(path).exists(path)

    def chmod(self, path: str, mode: int):
        return self.get_fs(path).chmod(path, mode)

    def cp(self, source: str, dest: str, force: bool = False):
        """Copy a file, handling cross-filesystem cases."""
        source_fs = self.get_fs(source)
        dest_fs = self.get_fs(dest)

        if source_fs != self.eos_fs and dest_fs != self.eos_fs:
            # Both local filesystems: direct copy
            return dest_fs.cp(source, dest, force=force)

        return self.eos_fs.cp(source, dest, force=force)

    def rm(self, path: str):
        return self.get_fs(path).rm(path)

    def ls(self, path: str, recursive: bool = False, pattern: Optional[str] = None):
        return self.get_fs(path).ls(path, recursive=recursive, pattern=pattern)

    def mkdir(self, path: str, exist_ok: bool = True):
        return self.get_fs(path).mkdir(path, exist_ok=exist_ok)
