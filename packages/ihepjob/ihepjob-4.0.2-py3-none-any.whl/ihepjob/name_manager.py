###############################################################################
# Author: Xuefeng DING <dingxf@ihep.ac.cn> @ IHEP-CAS
#
# Project: Qctr3 reco MT check
# Date: 2025 February 19th
# Version: v1.0
# Description:
#   name manager. to make sure names are uniform across the whole project
#
# Maintainer:
#   Xuefeng Ding <dingxf@ihep.ac.cn>
#
# All rights reserved. 2024 copyrighted.
###############################################################################
import os

from .config_manager import ConfigManager


class NameManager:
    def __init__(self, config: ConfigManager):
        self.config = config
        self._tmp_dir: str = "not_set_yet"

    @property
    def tmp_path(self) -> str:
        return self._tmp_dir

    @tmp_path.setter
    def tmp_path(self, value: str):
        self._tmp_dir = value

    @property
    def working_path(self) -> str:
        return self.config.working_dir

    @property
    def large_output_path(self) -> str:
        return os.path.join(self.config.large_output_dir, self.config.project)

    @property
    def small_output_path(self) -> str:
        return os.path.join(self.config.small_output_dir, self.config.project)

    def monitor_log_path(self, task_id: str) -> str:
        return os.path.join(
            self.config.small_output_dir,
            self.config.project,
            "monitor",
            f"{task_id}_monitor.json",
        )

    def out_path(self, task_id: str) -> str:
        return os.path.join(
            self.config.small_output_dir,
            self.config.project,
            "log",
            f"out_{task_id}.log",
        )

    def err_path(self, task_id: str) -> str:
        return os.path.join(
            self.config.small_output_dir,
            self.config.project,
            "log",
            f"err_{task_id}.log",
        )
