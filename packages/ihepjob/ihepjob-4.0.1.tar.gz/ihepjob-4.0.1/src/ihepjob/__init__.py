###############################################################################
# Author: Xuefeng DING <dingxf@ihep.ac.cn> @ IHEP-CAS
#
# Project: masive_job_submitter
# Date: 2025 February 24th
# Description:
#   name manager. to make sure names are uniform across the whole project
# History:
# v1.0 2025.02.24 dingxf@ihep.ac.cn first version.
#
# Maintainer:
#   Xuefeng Ding <dingxf@ihep.ac.cn>
#
# All rights reserved. 2024 copyrighted.
###############################################################################

__all__ = ["IHEPJob", "ConfigManager", "ProcessMonitor", "JobRunner", "FileSystemManager", "NameManager", "Job"]
from ._version import __version__, __version_tuple__  # noqa: F401 # type: ignore
from .config_manager import ConfigManager
from .job_runner import JobRunner
from .juno_filesystem import FileSystemManager
from .name_manager import NameManager
from .prepare_submit import IHEPJob
from .process_utility import ProcessMonitor
from .single_job import Job

__version__ = __version__
__version_tuple__ = __version_tuple__
