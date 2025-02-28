###############################################################################
# Author: Xuefeng DING <dingxf@ihep.ac.cn> @ IHEP-CAS
#
# Project: Qctr3 reco MT check
# Date: 2025 February 19th
# Version: v1.0
# Description:
#   run jobs
#
# Maintainer:
#   Xuefeng Ding <dingxf@ihep.ac.cn>
#
# All rights reserved. 2024 copyrighted.
###############################################################################
import os

from loguru import logger

from .config_manager import ConfigManager
from .juno_filesystem import FileSystemManager
from .name_manager import NameManager
from .process_utility import ProcessMonitor


class JobRunner:
    """Executes and monitors job commands."""

    def __init__(self, fs_manager: FileSystemManager, name_manager: NameManager, config_manager: ConfigManager):
        self.fs_manager = fs_manager
        self.name_manager = name_manager
        self.config = config_manager

    def run_job(self, script: str, inputs: list[str], args: list, task_id: str):
        """Execute a single job and handle its output."""
        monitor_log = self.name_manager.monitor_log_path(task_id)
        tmp_path = self.name_manager.tmp_path
        command = [script] + [tmp_path, task_id] + args
        command = [str(cmd) for cmd in command]

        logger.info(f"Starting [{task_id}] {script}")
        logger.debug(f"cwd <{os.getcwd()}>")
        logger.debug(f"tmp <{tmp_path}>")
        if isinstance(inputs, list):
            for input in inputs:
                tmp_input = os.path.join(tmp_path, os.path.basename(input))
                logger.debug(f"copy {input} => {tmp_input}")
                self.fs_manager.cp(input, tmp_input, force=True)
        logger.debug(f"Command <{' '.join(command)}>")
        monitor = ProcessMonitor(command, interval=5)
        monitor.monitor()
        monitor.save_data(monitor_log)

        output_config = {
            "large_output": self.name_manager.large_output_path,
            "small_output": self.name_manager.small_output_path,
        }
        for output_type, output_path in output_config.items():
            kept = set()
            patterns = getattr(self.config, output_type, None)
            for pattern in patterns:
                to_keep = self.fs_manager.ls(tmp_path, recursive=True, pattern=pattern)
                kept = kept.union(to_keep)
            logger.debug("Keeping files:")
            for path in kept:
                logger.debug(f"  {path}")
            for path in kept:
                file_name = os.path.basename(path)
                output_full_path = os.path.join(output_path, file_name)
                self.fs_manager.cp(path, output_full_path, force=True)
