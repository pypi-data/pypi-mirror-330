###############################################################################
# Author: Xuefeng DING <dingxf@ihep.ac.cn> @ IHEP-CAS
#
# Project: Qctr3 reco MT check
# Date: 2025 February 19th
# Version: v1.0
# Description:
#   End-to-end style Integration-test based on pytest for prepare_submit.py
#
# Maintainer:
#   Xuefeng Ding <dingxf@ihep.ac.cn>
#
# All rights reserved. 2024 copyrighted.
###############################################################################

import os
from unittest.mock import patch

import jinja2
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from ihepjob import IHEPJob


@pytest.fixture
def fs_fixture(fs: FakeFilesystem):
    source_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
    fs.add_real_directory(source_dir)
    fs.create_dir("/work")
    return fs


# Test the submission process
@patch("subprocess.run")
def test_ihepjob_fs(mock_run, fs_fixture):
    # Initialize IHEPJob with minimal parameters
    job = IHEPJob(
        project="test_project",
        working_dir="/work",
        large_output_dir="/large",
        small_output_dir="/small",
    )

    # Call setup to prepare the environment
    job.setup()

    # Verify setup created the submission script
    script_path = os.path.join(job.working_dir, "submit_job.sh")
    assert fs_fixture.exists(script_path), "Submission script was not created"
    with open(script_path) as f:
        script_content = f.read()
    assert "# Submission script for" in script_content, "Submission script content is incorrect"

    # Call run to trigger submission
    job.run()

    # Check that subprocess.run was called with the correct script path
    mock_run.assert_called_once_with([script_path])


def test_ihepjob_run_real(tmp_path):
    job = IHEPJob(
        project="test_project",
        working_dir=tmp_path.as_posix(),
        large_output_dir=tmp_path.as_posix(),
        small_output_dir=tmp_path.as_posix(),
    )
    job.setup()

    # Verify setup created the submission script
    script_path = os.path.join(job.working_dir, "submit_job.sh")
    assert os.path.exists(script_path), "Submission script was not created"
    with open(script_path) as f:
        script_content = f.read()
    assert "# Submission script for" in script_content, "Submission script content is incorrect"

    # Call run to trigger submission
    job.test_locally()


# Test edge case: missing template
@patch("subprocess.run")
def test_ihepjob_submit_missing_template(mock_run, fs_fixture):
    # Remove the template to simulate a failure
    job = IHEPJob(
        project="test_project",
        working_dir="/work",
        large_output_dir="/large",
        small_output_dir="/small",
    )
    fs_fixture.remove(os.path.join(job.default_templates_dir, "default", "submit_job.sh.jinja"))

    with pytest.raises(jinja2.exceptions.TemplateNotFound):
        job.setup()
