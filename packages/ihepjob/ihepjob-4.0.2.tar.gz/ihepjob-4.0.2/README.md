# ihepjob

**A Python package for preparing and submitting grid jobs at IHEP-CAS**

`ihepjob` simplifies the process of setting up and submitting jobs to a grid computing environment, such as HEP_submit, with support for configurable directories, YAML-based job definitions, and Jinja2 template rendering. Designed for researchers and students at the Institute of High Energy Physics (IHEP), Chinese Academy of Sciences (CAS), it provides a robust command-line interface for managing computational workflows.

Author: Xuefeng Ding <dingxf@ihep.ac.cn> @ IHEP-CAS

---

## Features

- **Grid Job Submission**: Generate and submit job scripts to grid systems with minimal configuration.
- **Flexible Configuration**: Define jobs and scripts via YAML files or Jinja2 templates.
- **Environment Integration**: Works seamlessly in local and grid environments with customizable output directories.
- **CLI Tools**: Two entry points: `ihepjob-submit` for batch submission and `ihepjob-single` for running individual jobs.

---

## Installation

### From PyPI (Coming Soon)

Once published on PyPI, install with:

```bash
pip install ihepjob
```

### From Git Repository

Clone the repository and install locally:

```bash
git clone git@code.ihep.ac.cn:neutrino-physics/ihepjob.git
cd ihepjob
pip install .
```

For development, use editable mode:

```bash
pip install -e .
```

#### Requirements

- Python 3.9+
- Dependencies: `loguru`, `jinja2`, `pyyaml`, `psutil` (automatically installed via `pip`)

---

## Usage

### Configuration

**Set EOS_MGM_URL**: Set the EOS_MGM_URL environment variable to the grid endpoint (e.g., `root://eosuser.cern.ch`).

```bash
export EOS_MGM_URL=root://eosuser.cern.ch
```

### Command-Line Interface

`ihepjob` provides two main commands:

1. **`ihepjob-submit`**:
   Prepares and submits a batch of jobs to the grid.

   ```bash
   ihepjob-submit --project my_project
   ```

   **Options**:

   - `--project`: Project name (required).
   - `--templates-dir`: Templates directory (default: `IHEPJOB_TEMPLATES_DIR` env var).
   - `--working-dir`: Working directory (default: `$PWD/<project>/notebook`, or `IHEPJOB_WORKING_DIR` env var).
   - `--large-output-dir`: Directory for large outputs (default: `<working_dir>/large_output`, or `IHEPJOB_LARGE_OUTPUT_DIR` env var).
   - `--small-output-dir`: Directory for small outputs (default: `<working_dir>/small_output`, or `IHEPJOB_SMALL_OUTPUT_DIR` env var).
   - `--jobs-yaml`: Path to external `jobs.yaml` (optional).
   - `--project-scripts-yaml`: Path to external `project_scripts.yaml` (optional).
   - `--test`: Run a single job locally instead of submitting (optional).
   - `--test-job-id`, `--test-proc-id`: Job and process IDs for local testing (default: 0).

   **Templates lookup order**

   1. `$PWD/templates`
   2. `$IHEP_TEMPLATES_DIR/project_name`
   3. `/path/to/ihepjob/tempaltes`

   **Example**:

   ```bash
   ihepjob-submit --project test_project --working-dir /tmp/test --large-output-dir /eos/large --small-output-dir /tmp/logs
   ```

2. **`ihepjob-single`**:
   Runs a single job locally (used internally by `submit_job.sh`).

   ```bash
   ihepjob-single --project-config config.yaml --jobs-config jobs.yaml --job-id 0 --proc-id 0
   ```

### Example Workflow

1. **Prepare and Submit Jobs**:

   ```bash
   ihepjob-submit --project my_project
   ```

   - Generates `config.yaml`, `jobs.yaml`, and `submit_job.sh` in `<cwd>/my_project/notebook/`.
   - Submits `submit_job.sh` to the grid.

2. **Test Locally**:
   ```bash
   ihepjob-submit --project my_project --test
   ```
   - Runs a single job locally using `ihepjob-single`.

---

## Configuration

### Default Directories

- **Working Directory**: `<current_dir>/<project>/notebook` (e.g., `/my/path/my_project/notebook`).
- **Large Output Directory**: `<working_dir>/large_output` (e.g., `/my/path/my_project/notebook/large_output`).
- **Small Output Directory**: `<working_dir>/small_output` (e.g., `/my/path/my_project/notebook/small_output`).

### Customizing Defaults

Override defaults using environment variables:

```bash
export IHEPJOB_WORKING_DIR=/custom/working
export IHEPJOB_LARGE_OUTPUT_DIR=/eos/large
export IHEPJOB_SMALL_OUTPUT_DIR=/tmp/logs
ihepjob-submit --project my_project
```

Or specify via command-line arguments:

```bash
ihepjob-submit --project my_project --working-dir /custom/working --large-output-dir /eos/large --small-output-dir /tmp/logs
```

### Templates and YAML Files

- **Templates**: Bundled in `templates/default/` (e.g., `jobs.yaml.jinja`, `submit_job.sh.jinja`) and rendered during setup.
- **External Configs**: Provide custom `jobs.yaml` or `project_scripts.yaml` with `--jobs-yaml` and `--project-scripts-yaml`.

---

## Project Structure

```
ihepjob/
├── src/
│   └── ihepjob/
│       ├── __init__.py
│       ├── prepare_submit.py
│       ├── single_job.py
│       ├── config_manager.py
│       ├── name_manager.py
│       ├── juno_filesystem.py
│       └── templates/
│           └── default/
│               ├── jobs.yaml.jinja
│               └── submit_job.sh.jinja
├── tests/
└── pyproject.toml
```

---

## Development

### Running Tests

Tests use `pytest` and `pyfakefs` to mock the filesystem:

```bash
pip install pytest pyfakefs
pytest tests/
```

### Contributing

1. Fork the repository: `git@code.ihep.ac.cn:neutrino-physics/ihepjob.git`.
2. Install in editable mode: `pip install -e .`.
3. Submit pull requests with changes.

### Building and Publishing

To build and upload to PyPI:

```bash
pip install build twine
python -m build
twine upload dist/*
```

---

## License

This project is licensed under the MIT License—see the `LICENSE` file for details.

---

## Contact

For issues or questions, contact Xuefeng Ding at <dingxf@ihep.ac.cn>.

---

### **Notes on the README**

- **Overview**: Highlights the purpose (grid job submission at IHEP-CAS) and key features.
- **Installation**: Covers PyPI (future), Git, and development modes, with clear commands.
- **Usage**: Provides CLI examples and options, reflecting your `prepare_submit.py` arguments.
- **Configuration**: Explains defaults and how to override them (env vars, CLI), avoiding your personal paths for professionalism.
- **Structure**: Matches your current layout (`src/ihepjob/`, `templates/`).
- **Development**: Includes testing and contribution instructions for collaborators/students.
- **License**: Assumes MIT (common for open-source)—update if you prefer another.

This `README.md` is polished, user-friendly, and ready for PyPI or Git sharing. Let me know if you want to tweak anything (e.g., add more examples, change the license)!
