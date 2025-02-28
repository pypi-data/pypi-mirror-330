###############################################################################
# Author: Xuefeng DING <dingxf@ihep.ac.cn> @ IHEP-CAS
#
# Project: Qctr reco MT check
# Date: 2025 February 19th
# Version: v1.0
# Description:
#   Unit-test based on pytest for python/config_manager.py
#
# Maintainer:
#   Xuefeng Ding <dingxf@ihep.ac.cn>
#
# All rights reserved. 2024 copyrighted.
###############################################################################

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from ihepjob import ConfigManager


def test_config_manager_init(fs: FakeFilesystem):
    # Create a fake YAML file with required fields
    yaml_content = r"""
    PROJECT: my_project
    working_dir: /tmp/working
    large_output_dir: /eos/large
    small_output_dir: /eos/small
    """
    fs.create_file("/fake/project.yaml", contents=yaml_content)

    # Test initialization with YAML file
    config = ConfigManager(project_yaml="/fake/project.yaml")
    assert config.project == "my_project"
    assert config.working_dir == "/tmp/working"
    assert config.large_output_dir == "/eos/large"
    assert config.small_output_dir == "/eos/small"
    assert config.large_output == [r".*\.root"]
    assert config.small_output == []


def test_config_manager_missing_args(fs: FakeFilesystem):
    # Test that project_yaml is required
    with pytest.raises(TypeError, match="missing.*required positional argument.*project_yaml"):
        ConfigManager()  # No arguments provided


def test_config_manager_attributes(fs: FakeFilesystem):
    # Create a fake YAML file with different values
    yaml_content = """
    PROJECT: test_proj
    working_dir: /custom/tmp
    large_output_dir: /custom/large
    small_output_dir: /custom/small
    """
    fs.create_file("/fake/project.yaml", contents=yaml_content)

    # Test attribute consistency
    config = ConfigManager(project_yaml="/fake/project.yaml")
    assert hasattr(config, "project")
    assert hasattr(config, "working_dir")
    assert hasattr(config, "large_output_dir")
    assert hasattr(config, "small_output_dir")
    assert not hasattr(config, "config_yaml")  # Should not exist
    assert config.project == "test_proj"
    assert config.working_dir == "/custom/tmp"
    assert config.large_output_dir == "/custom/large"
    assert config.small_output_dir == "/custom/small"



def test_config_manager_missing_yaml(fs: FakeFilesystem):
    # Test with non-existent YAML file
    with pytest.raises(FileNotFoundError, match="No such file or directory.*nonexistent.yaml"):
        ConfigManager(project_yaml="/fake/nonexistent.yaml")
