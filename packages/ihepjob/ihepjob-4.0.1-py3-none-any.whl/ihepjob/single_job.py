###############################################################################
# Author: Xuefeng DING <dingxf@ihep.ac.cn> @ IHEP-CAS
#
# Project: Qctr3 reco MT check
# Date: 2025 February 19th
# Version: v1.0
# Description:
#   run analysis jobs at IHEP @ lxlogin.ihep.ac.cn
#   this is the entrance script executed for on ProcId
#
# Maintainer:
#   Xuefeng Ding <dingxf@ihep.ac.cn>
#
# All rights reserved. 2024 copyrighted.
###############################################################################
import argparse
import tempfile
from typing import Optional

import yaml
from loguru import logger

from .config_manager import ConfigManager
from .job_runner import JobRunner
from .juno_filesystem import FileSystemManager
from .name_manager import NameManager


class Job:
    """Manages the lifecycle of a single job."""

    def __init__(
        self,
        project_yaml: str,
        jobs_yaml: str,
        job_id: int = 0,
        proc_id: int = 0,
        extra_args: Optional[list[str]] = None,
    ):
        self.project_yaml = project_yaml
        self.jobs_yaml = jobs_yaml
        self.job_id = job_id
        self.proc_id = proc_id
        self.extra_args = extra_args or []

        self.config = ConfigManager(project_yaml)
        self.jobs_yaml = jobs_yaml

        self.fs_manager = FileSystemManager()
        self.name_manager = NameManager(self.config)
        self.runner = JobRunner(self.fs_manager, self.name_manager, self.config)
        self.todo: list[tuple] = []

    def __enter__(self):
        self._tmp_dir = tempfile.TemporaryDirectory()
        self.name_manager.tmp_path = self._tmp_dir.name
        self.setup()
        return self

    def __exit__(self, exc_type, exc_val, tb):
        self._tmp_dir.cleanup()
        if exc_type:
            logger.exception(f"Job failed: {exc_val}")
        else:
            logger.info(f"Cleaned up {self._tmp_dir.name}")

    def setup(self):
        with open(self.jobs_yaml) as f:
            self.tasks = yaml.safe_load(f)
        tasks = self.dispatch_job(self.job_id, self.proc_id, self.tasks)
        for task in tasks:
            script = task.get("script")
            inputs = task.get("inputs")
            if isinstance(inputs, str):
                inputs = [inputs]
            inputs = inputs if inputs else []
            task_args = task.get("args")
            task_args = task_args if task_args else []
            task_id = task["task_id"]
            args = task_args + self.extra_args
            self.todo.append((script, inputs, args, task_id))
            logger.debug(self.todo[-1])

    def run(self):
        logger.info(
            f"Lauching {self.config.project} job-id {self.job_id} proc-id {self.proc_id} "
            f"with {len(self.todo)} / {len(self.tasks)} tasks"
        )
        try:
            for script, inputs, args, task_id in self.todo:
                self.runner.run_job(script, inputs, args, task_id)
        except Exception as e:
            logger.exception(f"Job failed: {e}")
        logger.info("Job completed")

    @staticmethod
    def dispatch_job(job_id: int, proc_id: int, tasks: list[dict]) -> list[dict]:
        # Corrected return type to list[dict] since jobs_yaml contains dicts
        return [tasks[job_id]] if proc_id == 0 and job_id < len(tasks) else []


def main():
    parser = argparse.ArgumentParser(description="Run a single job")
    parser.add_argument("--project-config", required=True)
    parser.add_argument("--jobs-config", required=True)
    parser.add_argument("--job-id", type=int, default=0)
    parser.add_argument("--proc-id", type=int, default=0)
    args, unknown = parser.parse_known_args()

    with Job(
        args.project_config,
        args.jobs_config,
        args.job_id,
        args.proc_id,
        unknown,
    ) as job:
        job.run()


if __name__ == "__main__":
    main()
