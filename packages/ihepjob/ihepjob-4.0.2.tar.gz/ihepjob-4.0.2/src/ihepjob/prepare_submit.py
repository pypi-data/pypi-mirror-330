###############################################################################
# Author: Xuefeng DING <dingxf@ihep.ac.cn> @ IHEP-CAS
#
# Project: Qctr3 reco MT check
# Date: 2025 February 19th
# Version: v1.0
# Description:
#   submit jobs at IHEP @ lxlogin.ihep.ac.cn
#
# Maintainer:
#   Xuefeng Ding <dingxf@ihep.ac.cn>
#
# All rights reserved. 2024 copyrighted.
###############################################################################
import argparse
import os
import subprocess
import sys
import tempfile
from importlib.resources import files
from typing import Optional

import yaml
from jinja2 import Environment, FileSystemLoader
from loguru import logger

from .config_manager import ConfigManager
from .juno_filesystem import FileSystemManager
from .name_manager import NameManager


class IHEPJob:
    def __init__(
        self,
        project: str,
        working_dir: str,
        large_output_dir: str,
        small_output_dir: str,
        templates_dir: Optional[str] = None,
        jobs_yaml: Optional[str] = None,  # Optional external job config
        project_config_yaml: Optional[str] = None,  # Optional external script config
    ):
        """Initialize IHEPJob with project settings and optional external configs."""
        self.project = project
        self.working_dir = working_dir
        self.large_output_dir = large_output_dir
        self.small_output_dir = small_output_dir
        self.jobs_yaml = jobs_yaml
        self.project_config_yaml = project_config_yaml
        logger.debug(f"default_templates_dir {self.default_templates_dir}")

        # Generate a temporary project.yaml file for ConfigManager
        with tempfile.TemporaryDirectory() as temp_dir:
            project_yaml_path = os.path.join(temp_dir, "temp_project.yaml")
            project_config = {
                "PROJECT": self.project,
                "working_dir": self.working_dir,
                "large_output_dir": self.large_output_dir,
                "small_output_dir": self.small_output_dir,
            }
            with open(project_yaml_path, "w") as f:
                yaml.dump(project_config, f)

            # Initialize ConfigManager with the generated YAML file
            self.config = ConfigManager(project_yaml=project_yaml_path)

        self.name_manager = NameManager(self.config)
        self.filesystem = FileSystemManager()

        # Set up Jinja environment with project-specific and default template dirs
        self.template_dirs = [
            dir_path
            for dir_path in [
                os.path.join(templates_dir, project) if templates_dir else None,
                os.path.join(os.getcwd(), "templates"),
                os.path.join(self.default_templates_dir, project),
                os.path.join(self.default_templates_dir, "default"),
            ]
            if dir_path
        ]
        self.template_env = Environment(loader=FileSystemLoader(self.template_dirs))

    def load_config(self):
        if self.project_config_yaml and os.path.exists(self.project_config_yaml):
            with open(self.project_config_yaml) as f:
                self.project_config = yaml.safe_load(f)
            logger.info(f"Load config from external project_config.yaml from {self.project_config_yaml}")
        else:
            template_path = "project_config.yaml"
            template = self.template_env.get_template(template_path)
            scripts_content = template.render()
            self.project_config = yaml.safe_load(scripts_content)
        config_data = {
            "PROJECT": self.project,
            "working_dir": self.working_dir,
            "large_output_dir": self.large_output_dir,
            "small_output_dir": self.small_output_dir,
            "templates_dir": self.template_dirs,
        }
        self.project_config.update(config_data)

    def setup_dirs(self):
        """Create necessary directories."""
        try:
            paths = [
                self.working_dir,
                os.path.join(self.small_output_dir, self.project, "monitor"),
                os.path.join(self.small_output_dir, self.project, "log"),
                os.path.join(self.large_output_dir, self.project),
            ]
            for path in paths:
                self.filesystem.mkdir(path, exist_ok=True)
        except Exception as e:
            logger.exception(e)

    def generate_config_yaml(self):
        """Generate config.yaml with project-wide settings."""
        config_path = os.path.join(self.working_dir, "config.yaml")
        with open(config_path, "w") as f:
            yaml.dump(self.project_config, f)
        logger.info(f"Generated {config_path}")
        return config_path

    def generate_jobs_yaml(self):
        """Generate jobs.yaml from external file or Jinja template."""
        jobs_path = os.path.join(self.working_dir, "jobs.yaml")

        if self.jobs_yaml and os.path.exists(self.jobs_yaml):
            with open(self.jobs_yaml) as f:
                jobs_data = yaml.safe_load(f)
            with open(jobs_path, "w") as f:
                yaml.dump(jobs_data, f)
            logger.info(f"Copied external jobs.yaml from {self.jobs_yaml} to {jobs_path}")
        else:
            template_path = "jobs.yaml.jinja"
            template = self.template_env.get_template(template_path)
            jobs_content = template.render(
                project=self.project,
                working_dir=self.working_dir,
                name_manager=self.name_manager,
            )
            with open(jobs_path, "w") as f:
                f.write(jobs_content)
            logger.info(f"Generated {jobs_path}")
        return jobs_path

    def generate_scripts(self):
        """Generate shell scripts from project_scripts.yaml or external override."""
        jobs = self.get_jobs_list()  # Get jobs from jobs.yaml
        for script in self.project_config.get("scripts", []):
            name = script["name"]
            template_name = script["template"]
            logger.debug(f"Parsing {template_name}")
            context = script.get("context", {})
            context.update(
                {
                    "python_exe": sys.executable,
                    "config_yaml": os.path.join(self.working_dir, "config.yaml"),
                    "jobs_yaml": os.path.join(self.working_dir, "jobs.yaml"),
                    "name_manager": self.name_manager,
                    "jobs": jobs,  # Pass the list of jobs
                    "cwd": os.getcwd(),
                }
            )  # for submit_job.sh, do not remove this

            template = self.template_env.get_template(template_name)
            script_path = os.path.join(self.working_dir, name)
            with open(script_path, "w") as f:
                f.write(template.render(**context))
            self.filesystem.chmod(script_path, 0o755)
            logger.info(f"Generated {script_path}")

    def get_jobs_list(self):
        jobs_path = os.path.join(self.working_dir, "jobs.yaml")
        with open(jobs_path) as f:
            return yaml.safe_load(f)

    def setup(self):
        """Set up directories and generate all necessary files."""
        self.load_config()
        self.setup_dirs()
        self.generate_config_yaml()
        self.generate_jobs_yaml()
        self.generate_scripts()

    def run(self):
        """Execute the submit_job.sh script."""
        script_path = os.path.join(self.working_dir, "submit_job.sh")
        subprocess.run([script_path])

    def test_locally(self, job_id=0, proc_id=0):
        """Run a single job locally for testing."""
        config_yaml = os.path.join(self.working_dir, "config.yaml")
        jobs_yaml = os.path.join(self.working_dir, "jobs.yaml")

        # Construct the command using the ihepjob-single entry point
        command = [
            "ihepjob-single",
            "--project-config",
            config_yaml,
            "--jobs-config",
            jobs_yaml,
            "--job-id",
            str(job_id),
            "--proc-id",
            str(proc_id),
        ]
        logger.info(f"Running local test with command: {' '.join(command)}")
        subprocess.run(command, check=True)

    @property
    def default_templates_dir(self):
        templates_path = files("ihepjob").joinpath("templates")
        if templates_path.is_dir():
            return str(templates_path)
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "templates"))


def main():
    parser = argparse.ArgumentParser(description="Prepare and submit grid jobs")
    parser.add_argument("--project", required=True, help="Project name")

    # Set working_dir default if not provided
    parser.add_argument(
        "--templates-dir",
        default=os.getenv("IHEPJOB_TEMPLATES_DIR", None),
        help="Templates directory (default: `IHEPJOB_TEMPLATES_DIR` env var)",
    )
    parser.add_argument(
        "--working-dir",
        default=None,
        help="Working directory (default: $PWD/project_name, or IHEPJOB_WORKING_DIR env var)",
    )
    parser.add_argument(
        "--large-output-dir",
        default=None,
        help="Large output directory (default: working_dir/large_output, or IHEPJOB_LARGE_OUTPUT_DIR env var)",
    )
    parser.add_argument(
        "--small-output-dir",
        default=None,
        help="Small output directory (default: working_dir/small_output, or IHEPJOB_SMALL_OUTPUT_DIR env var)",
    )
    parser.add_argument("--jobs-yaml", default=None, help="Path to external jobs YAML (optional)")
    parser.add_argument(
        "--project-config-yaml",
        default=None,
        help="Path to external project config YAML (optional)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Dry run")
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run a single job locally for testing instead of submitting to grid",
    )
    parser.add_argument(
        "--test-job-id",
        type=int,
        default=0,
        help="Job ID for local testing (default: 0)",
    )
    parser.add_argument(
        "--test-proc-id",
        type=int,
        default=0,
        help="Proc ID for local testing (default: 0)",
    )
    args = parser.parse_args()

    working_dir = (
        args.working_dir
        if args.working_dir
        else os.getenv("IHEPJOB_WORKING_DIR", os.path.join(os.getcwd(), args.project))
    )
    large_output_dir = (
        args.large_output_dir
        if args.large_output_dir
        else os.getenv("IHEPJOB_LARGE_OUTPUT_DIR", os.path.join(working_dir, "large_output"))
    )
    small_output_dir = (
        args.small_output_dir
        if args.small_output_dir
        else os.getenv("IHEPJOB_SMALL_OUTPUT_DIR", os.path.join(working_dir, "small_output"))
    )

    job = IHEPJob(
        project=args.project,
        working_dir=working_dir,
        large_output_dir=large_output_dir,
        small_output_dir=small_output_dir,
        templates_dir=args.templates_dir,
        jobs_yaml=args.jobs_yaml,
        project_config_yaml=args.project_config_yaml,
    )

    job.setup()

    if args.test:
        job.test_locally(job_id=args.test_job_id, proc_id=args.test_proc_id)
    elif not args.dry_run:
        job.run()


if __name__ == "__main__":
    main()
