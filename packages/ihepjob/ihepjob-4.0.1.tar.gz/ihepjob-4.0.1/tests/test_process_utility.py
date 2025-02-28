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

import json
from io import StringIO
from time import time
from unittest.mock import MagicMock, patch

from pyfakefs.fake_filesystem import FakeFilesystem

from ihepjob import ProcessMonitor


def test_process_monitor_success(fs: FakeFilesystem):
    command = ["echo", "Hello, World!"]
    output_file = "/fake/path/monitor_log.json"
    fs.create_dir("/fake/path")

    # Mock subprocess.Popen with realistic stdout/stderr
    fake_process = MagicMock(pid=1234, wait=MagicMock(return_value=0))
    fake_process.stdout = StringIO("Hello, World!\n")
    fake_process.stderr = StringIO()
    fake_process.stdout.fileno = lambda: 1
    fake_process.stderr.fileno = lambda: 2

    # Mock psutil.Process with realistic return values
    fake_child = MagicMock()
    fake_child.threads.return_value = [
        MagicMock(id=1001, user_time=0.1, system_time=0.05),
        MagicMock(id=1002, user_time=0.2, system_time=0.1),
    ]
    mem_info_mock = MagicMock()
    mem_info_mock.vms = 1024 * 1024
    mem_info_mock.rss = 512 * 1024
    cpu_times_mock = MagicMock()
    cpu_times_mock.user = 2
    cpu_times_mock.system = 1
    fake_psutil_process = MagicMock()
    fake_psutil_process.memory_info.return_value = mem_info_mock
    fake_psutil_process.cpu_times.return_value = cpu_times_mock
    fake_psutil_process.create_time.return_value = time() - 60
    fake_psutil_process.status.side_effect = ["running", "zombie"]
    fake_psutil_process.children.return_value = [fake_child, fake_child]
    fake_child.memory_info.return_value = mem_info_mock
    fake_child.cpu_times.return_value = cpu_times_mock

    with (
        patch("ihepjob.process_utility.Popen", return_value=fake_process),
        patch("ihepjob.process_utility.psutil.Process", return_value=fake_psutil_process),
        patch("ihepjob.process_utility.sleep", return_value=None),
        patch("ihepjob.process_utility.fcntl"),
        patch("ihepjob.process_utility.select", return_value=([fake_process.stdout], [], [])),
    ):
        monitor = ProcessMonitor(command, interval=0.1)
        monitor.monitor()
        monitor.save_data(output_file)

    assert fs.exists(output_file)
    with open(output_file) as f:
        data = json.load(f)
    assert len(data) > 0
    assert "vsz" in data[0]
    assert "rss" in data[0]
    assert "cpu" in data[0]
    assert "elapsed" in data[0]
    assert isinstance(data[0]["threads_user"], dict)
    assert isinstance(data[0]["threads_system"], dict)
    assert data[0]["threads_user"] == {"1001": 0.1, "1002": 0.2}
    assert data[0]["threads_system"] == {"1001": 0.05, "1002": 0.1}
