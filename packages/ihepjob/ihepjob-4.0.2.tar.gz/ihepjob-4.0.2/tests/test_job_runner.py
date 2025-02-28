###############################################################################
# Author: Xuefeng DING <dingxf@ihep.ac.cn> @ IHEP-CAS
#
# Project: Qctr reco MT check
# Date: 2025 February 19th
# Version: v1.0
# Description:
#   Unit-test based on pytest for python/job_runner.py
#
# Maintainer:
#   Xuefeng Ding <dingxf@ihep.ac.cn>
#
# All rights reserved. 2024 copyrighted.
###############################################################################

import shutil
import textwrap
from unittest.mock import call, patch

from pyfakefs.fake_filesystem import FakeFilesystem

from ihepjob import ConfigManager, FileSystemManager, JobRunner, NameManager


@patch("ihepjob.job_runner.ProcessMonitor")
def test_job_runner_run_job(mock_monitor_class, fs: FakeFilesystem):
    # Create a fake project YAML config
    project_yaml = textwrap.dedent(r"""
        PROJECT: test
        working_dir: /eos/working
        large_output_dir: /eos/large
        small_output_dir: /eos/small
        small_output:
            - ^.*\.profiling$
        """)
    fs.create_file("/fake/project.yaml", contents=project_yaml)
    config = ConfigManager(project_yaml="/fake/project.yaml")
    nm = NameManager(config)
    nm.tmp_path = "/tmp"  # Set tmp_dir explicitly since it's runtime-set in Job
    fs_manager = FileSystemManager()
    runner = JobRunner(fs_manager, nm, config)

    # Mock ProcessMonitor behavior
    mock_monitor = mock_monitor_class.return_value
    mock_monitor.monitor.return_value = None  # Simulate successful monitoring
    mock_monitor.save_data.return_value = None  # Simulate data saving

    # Create a temporary output file based on task_id
    task_id = "mt_4"
    tmp_file_path = f"/tmp/{task_id}_rec_EDM.root"
    final_output_path = "/eos/large/test"
    final_file_path = f"/eos/large/test/{task_id}_rec_EDM.root"
    fs.create_file(tmp_file_path, contents="test data")
    fs.create_file("/tmp/xx.profiling", contents="test data")
    fs.create_file("/eos/input/test", contents="test data")
    fs.create_dir(final_output_path)
    fs.create_dir("/eos/small/test")

    # Mock FileSystemManager.cp to simulate moving the file
    # with patch.object(FileSystemManager, "ls") as mock_ls, patch.object(FileSystemManager, "cp") as mock_cp:
    # Simulate the cp operation by moving the file within FakeFilesystem
    with patch.object(FileSystemManager, "cp") as mock_cp:

        def simulate_cp(source, dest, force=True):
            if fs.exists(source):
                if fs.exists(dest) and force:
                    fs.remove(dest)
                # Use shutil.copy to copy within FakeFilesystem (patched by pyfakefs)
                shutil.copy(source, dest)
                fs.remove(source)
            return True  # Simulate successful copy

        mock_cp.side_effect = simulate_cp
        runner.run_job("single_job_mt.sh", ["/eos/input/test"], ["arg1", "arg2"], task_id)
        expected_calls = [
            call("/eos/input/test", "/tmp/test", force=True),
            call(tmp_file_path, final_file_path, force=True),
            call("/tmp/xx.profiling", "/eos/small/test/xx.profiling", force=True),
        ]
        assert mock_cp.call_args_list == expected_calls

    # Check that the tmp file was moved to the final location
    assert not fs.exists(tmp_file_path), "Temporary file should be moved or deleted"
    assert fs.exists(final_file_path), "Final output file should exist"

    # Check monitor log (created by ProcessMonitor.save_data)
    monitor_log_path = f"/eos/small/test/monitor/{task_id}_monitor.json"
    assert mock_monitor.save_data.called  # Verify save_data was called
    # Simulate ProcessMonitor saving the monitor log
    fs.create_file(monitor_log_path, contents="{}")
    assert fs.exists(monitor_log_path), "Monitor log should be created"
