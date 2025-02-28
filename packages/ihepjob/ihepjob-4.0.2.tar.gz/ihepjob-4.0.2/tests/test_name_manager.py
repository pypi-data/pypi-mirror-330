###############################################################################
# Author: Xuefeng DING <dingxf@ihep.ac.cn> @ IHEP-CAS
#
# Project: Qctr reco MT check
# Date: 2025 February 19th
# Version: v1.0
# Description:
#   Unit-test based on pytest for python/name_manager.py
#
# Maintainer:
#   Xuefeng Ding <dingxf@ihep.ac.cn>
#
# All rights reserved. 2024 copyrighted.
###############################################################################

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from ihepjob import ConfigManager, NameManager


@pytest.fixture
def config(fs: FakeFilesystem):
    # Create a fake YAML file for ConfigManager
    yaml_content = """
    PROJECT: test_project
    source_dir: /source
    working_dir: /tmp/working
    large_output_dir: /eos/large
    small_output_dir: /eos/small
    """
    fs.create_file("/fake/project.yaml", contents=yaml_content)
    return ConfigManager(project_yaml="/fake/project.yaml")


@pytest.fixture
def name_manager(config):
    return NameManager(config)


def test_name_manager_paths(config, name_manager, fs: FakeFilesystem):
    # Set tmp_dir for testing
    name_manager.tmp_path = "/tmp/test"

    # Test static paths
    assert name_manager.tmp_path == "/tmp/test"
    assert name_manager.working_path == "/tmp/working"
    assert name_manager.large_output_path == "/eos/large/test_project"
    assert name_manager.small_output_path == "/eos/small/test_project"

    # Test dynamic paths with job_id
    assert name_manager.monitor_log_path("mt_1") == "/eos/small/test_project/monitor/mt_1_monitor.json"
    assert name_manager.out_path("mt_1") == "/eos/small/test_project/log/out_mt_1.log"
    assert name_manager.err_path("mt_1") == "/eos/small/test_project/log/err_mt_1.log"
