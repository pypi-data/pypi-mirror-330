###############################################################################
# Author: Xuefeng DING <dingxf@ihep.ac.cn> @ IHEP-CAS
#
# Project: Qctr reco MT check
# Date: 2025 February 19th
# Version: v1.0
# Description:
#   Unit-test based on pytest for python/single_job.py
#
# Maintainer:
#   Xuefeng Ding <dingxf@ihep.ac.cn>
#
# All rights reserved. 2024 copyrighted.
###############################################################################

import textwrap
from unittest.mock import patch

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from ihepjob import Job


@pytest.fixture
def project_config(fs: FakeFilesystem):
    # Fake project YAML for ConfigManager
    project_yaml_content = textwrap.dedent("""\
        PROJECT: test_project
        working_dir: /tmp/working
        large_output_dir: /eos/large
        small_output_dir: /eos/small
    """)
    fs.create_file("/fake/project.yaml", contents=project_yaml_content)
    return "/fake/project.yaml"


@pytest.fixture
def jobs_config(fs: FakeFilesystem):
    # Fake jobs YAML with task definitions
    jobs_yaml_content = textwrap.dedent("""\
        - script: single_job_mt.sh
          args: ["/input", "/output", "100"]
          inputs: ["/eos/input/file1", "/eos/input/file2" ]
          task_id: mt_1
        - script: single_job_sr.sh
          args: ["/input", "/output", "50"]
          inputs: ["/eos/input/file3", "/eos/input/file4" ]
          task_id: sr_1
    """)
    fs.create_file("/fake/jobs.yaml", contents=jobs_yaml_content)
    return "/fake/jobs.yaml"


@pytest.fixture
def job(project_config, jobs_config):
    with Job(
        project_yaml=project_config,
        jobs_yaml=jobs_config,
        job_id=0,
        proc_id=0,
        extra_args=["--extra"],
    ) as analysis_job:
        yield analysis_job


def test_setup(job, fs: FakeFilesystem):
    # Verify setup creates tasks from jobs_yaml
    assert len(job.todo) == 1, "Should have one task for job_id=0, proc_id=0"
    script, inputs, args, task_id = job.todo[0]
    assert script == "single_job_mt.sh"
    assert inputs == ["/eos/input/file1", "/eos/input/file2"]
    assert args == ["/input", "/output", "100", "--extra"]
    assert task_id == "mt_1"
    assert fs.exists(job.name_manager.tmp_path), "Temporary directory should be created"


@patch("ihepjob.single_job.JobRunner.run_job")
def test_run(mock_run_job, job, fs: FakeFilesystem):
    # Simulate running the job
    job.run()
    assert mock_run_job.called
    script, inputs, args, task_id = job.todo[0]
    mock_run_job.assert_called_once_with(script, inputs, args, task_id)


def test_dispatch_job(job):
    # Test dispatch_job with mock config
    config_data = [
        {"script": "single_job_mt.sh", "args": ["arg1"], "task_id": "mt_1"},
        {"script": "single_job_sr.sh", "args": ["arg2"], "task_id": "sr_1"},
    ]
    assert Job.dispatch_job(0, 0, config_data) == [config_data[0]]
    assert Job.dispatch_job(1, 0, config_data) == [config_data[1]]
    assert Job.dispatch_job(0, 1, config_data) == []
    assert Job.dispatch_job(2, 0, config_data) == []


def test_job_init_with_custom_yaml(fs: FakeFilesystem):
    # Test initialization with custom YAML files
    project_yaml_content = """
    PROJECT: custom_project
    working_dir: /custom/working
    large_output_dir: /custom/large
    small_output_dir: /custom/small
    """
    jobs_yaml_content = """
    - script: custom_script.sh
      args: ["/custom/input", "/custom/output"]
      task_id: custom_task
    """
    fs.create_file("/fake/custom_project.yaml", contents=project_yaml_content)
    fs.create_file("/fake/custom_jobs.yaml", contents=jobs_yaml_content)

    with Job(
        project_yaml="/fake/custom_project.yaml",
        jobs_yaml="/fake/custom_jobs.yaml",
        job_id=0,
        proc_id=0,
    ) as custom_job:
        assert custom_job.config.project == "custom_project"
        assert len(custom_job.todo) == 1
        assert custom_job.todo[0][3] == "custom_task"
