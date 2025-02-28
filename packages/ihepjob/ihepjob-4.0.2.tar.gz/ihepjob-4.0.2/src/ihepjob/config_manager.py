###############################################################################
# Author: Xuefeng DING <dingxf@ihep.ac.cn> @ IHEP-CAS
#
# Project: Qctr3 reco MT check
# Date: 2025 February 19th
# Description:
#   holding configuration data for the project.
#
# History:
# v1.0 2025.02.19 dingxf@ihep.ac.cn first version
#
# Maintainer:
#   Xuefeng Ding <dingxf@ihep.ac.cn>
#
# All rights reserved. 2024 copyrighted.
###############################################################################

import yaml
from loguru import logger


class ConfigManager:
    def __init__(self, project_yaml: str):
        with open(project_yaml) as f:
            config_data = yaml.safe_load(f)
        self.project = config_data["PROJECT"]
        self.working_dir = config_data["working_dir"]
        self.large_output_dir = config_data["large_output_dir"]
        self.small_output_dir = config_data["small_output_dir"]
        self.large_output = config_data.get("large_output", [r".*\.root"])
        self.small_output = config_data.get("small_output", [])
        for line in str(self).split("\n"):
            logger.debug(line)

    def __repr__(self):
        return yaml.dump(self.__dict__).strip()
