###############################################################################
# Author: Xuefeng DING <dingxf@ihep.ac.cn> @ IHEP-CAS
#
# Project: Qctr3 reco MT check
# Date: 2025 February 19th
# Description:
#   utility to monitor process
# History:
# v1.0 2025.02.19 dingxf@ihep.ac.cn first version.
# v1.1 2025.02.22 dingxf@ihep.ac.cn strip out n_th.
#
# Maintainer:
#   Xuefeng Ding <dingxf@ihep.ac.cn>
#
# All rights reserved. 2024 copyrighted.
###############################################################################
import json
import os
from fcntl import F_GETFL, F_SETFL, fcntl
from select import select
from subprocess import PIPE, Popen, TimeoutExpired
from time import sleep, time

import psutil
from loguru import logger


class OutputFetcher:
    def __init__(self, process: Popen):
        self.process = process
        self.stdout_buffer = b""
        self.stderr_buffer = b""

    def __enter__(self):
        # Set stdout and stderr to non-blocking
        logger.level("STDOUT", no=15, color="<cyan>")  # Between DEBUG (10) and INFO (20)
        logger.level("STDERR", no=16, color="<magenta>")
        for stream in [self.process.stdout, self.process.stderr]:
            if stream:  # Ensure stream exists
                fd = stream.fileno()
                flags = fcntl(fd, F_GETFL)
                fcntl(fd, F_SETFL, flags | os.O_NONBLOCK)
        return self

    def __exit__(self, exc_type, exc_val, tb):
        if exc_type is not None:
            logger.exception(exc_val)
        else:
            logger.info("OutputFetcher cleaning up normally.")
        if self.stdout_buffer:
            logger.log("STDOUT", self.stdout_buffer.decode("utf-8", errors="replace").strip())
        if self.stderr_buffer:
            logger.log("STDERR", self.stderr_buffer.decode("utf-8", errors="replace").strip())

    def fetch_stdout_stderr(self):
        """Fetches stdout and stderr of the process in a non-blocking way."""
        read_fds, _, _ = select([self.process.stdout, self.process.stderr], [], [], 0.1)
        for stream in read_fds:
            if stream is self.process.stdout:
                while True:
                    try:
                        chunk = os.read(stream.fileno(), 4096)
                        if not chunk:
                            break
                        self.stdout_buffer += chunk
                    except BlockingIOError:
                        break
                lines = self.stdout_buffer.split(b"\n")
                for line in lines[:-1]:
                    logger.log("STDOUT", line.decode("utf-8", errors="replace").strip())
                self.stdout_buffer = lines[-1]
            elif stream is self.process.stderr:
                while True:
                    try:
                        chunk = os.read(stream.fileno(), 4096)
                        if not chunk:
                            break
                        self.stderr_buffer += chunk
                    except BlockingIOError:
                        break
                lines = self.stderr_buffer.split(b"\n")
                for line in lines[:-1]:
                    logger.log("STDERR", line.decode("utf-8", errors="replace").strip())
                self.stderr_buffer = lines[-1]


class ProcessMonitor:
    def __init__(self, command, interval=5):
        self.command = [str(cmd) for cmd in command]
        self.interval = interval
        self.data = []
        self.process = None
        self.p = None

    def start(self):
        """Start the process and initialize psutil handle."""
        self.process = Popen(self.command, stdout=PIPE, stderr=PIPE)
        self.p = psutil.Process(self.process.pid)

    def collect_process_data(self):
        """Collect process and thread data, aggregating across parent and children."""
        try:
            # Parent process data
            parent_info = self.p.as_dict(attrs=["pid", "ppid", "status", "cpu_times", "create_time"])
            logger.info(f"process: {parent_info}")

            # Aggregate memory and CPU across parent and children
            total_vms = self.p.memory_info().vms
            total_rss = self.p.memory_info().rss
            total_cpu = self.p.cpu_times().user + self.p.cpu_times().system
            elapsed_time = time() - self.p.create_time()

            children = self.p.children(recursive=True)
            threads_user = {}
            threads_system = {}

            for child in children:
                try:
                    total_vms += child.memory_info().vms
                    total_rss += child.memory_info().rss
                    total_cpu += child.cpu_times().user + child.cpu_times().system
                    for t in child.threads():
                        threads_user[t.id] = t.user_time
                        threads_system[t.id] = t.system_time
                except psutil.NoSuchProcess:
                    logger.debug(f"Child {child.pid} disappeared during collection")
                    continue

            if threads_user:
                logger.debug(f"Threads user time: {threads_user}")
                logger.debug(f"Threads system time: {threads_system}")

            self.data.append(
                {
                    "vsz": total_vms,
                    "rss": total_rss,
                    "cpu": total_cpu,
                    "elapsed": elapsed_time,
                    "threads_user": threads_user,
                    "threads_system": threads_system,
                }
            )
            logger.debug(f"Collected data point: {self.data[-1]}")
            return True
        except psutil.NoSuchProcess:
            logger.info(f"Process {self.p.pid} no longer exists.")
            return False

    def is_process_alive(self):
        """Check if the process or its children are still running."""
        try:
            status = self.p.status()
            if status == psutil.STATUS_ZOMBIE:
                logger.debug(f"Process {self.p.pid} is a zombie, reaping...")
                return False
            children = self.p.children(recursive=True)
            return self.p.is_running() or bool(children)
        except psutil.NoSuchProcess:
            logger.info(f"Process {self.p.pid} no longer exists.")
            return False

    def cleanup(self):
        """Clean up process resources."""
        for stream in (self.process.stdout, self.process.stderr):
            if stream and not stream.closed:
                stream.close()
        try:
            return_code = self.process.wait(timeout=10)
            logger.info(f"Process {self.p.pid} exited with code {return_code}")
        except TimeoutExpired:
            logger.warning(f"Process {self.p.pid} did not exit, forcing kill...")
            self.p.kill()
            self.process.wait()

    def monitor(self):
        """Monitor the process and collect data."""
        self.start()
        with OutputFetcher(self.process) as utility:
            try:
                while True:
                    utility.fetch_stdout_stderr()
                    if not self.is_process_alive():
                        break
                    if not self.collect_process_data():
                        break
                    sleep(self.interval)
                utility.fetch_stdout_stderr()
            except Exception as e:
                logger.exception(f"Monitoring failed: {e}")
            finally:
                self.cleanup()

    def save_data(self, filepath):
        """Save collected data to a JSON file."""
        if self.data:
            try:
                with open(filepath, "w") as f:
                    json.dump(self.data, f)
                logger.info(f"Monitoring data saved to {filepath}")
            except Exception as e:
                logger.debug("Trying to dump:")
                logger.debug(self.data)
                logger.exception(f"Failed to save data to {filepath}: {e}")
        else:
            logger.warning("No monitoring data collected.")
