# PySyncPack

An enhanced rsync wrapper with native VCS and .gitignore support, providing both a Python API and a command-line interface.

*Caveat Emptor*: The code in this package was developed and tested by a human, but may still contain bugs. Documentation was written largely by a machine (Claude 3.5 Sonnet), and may contain errors.

## Features

- Smart ignore file handling:
  - Native support for `.gitignore` and `.syncignore`
  - Optional CVS exclude patterns
  - Flexible parsing options for ignore files
- Common dev exclusions by default
- Both CLI + Python API interfaces
- SSH support for remote syncing

## Installation

### Using pip (Recommended)

```bash
pip install git+https://github.com/colinconwell/PySyncPack.git
```

### Using Poetry

```bash
poetry add git+https://github.com/colinconwell/PySyncPack.git
```

### CLI Tool Only

If you only want the command-line tool without installing the Python package:

```bash
curl -O https://raw.githubusercontent.com/colinconwell/PySyncPack/main/scripts/cli_install.sh
chmod +x cli_install.sh
./cli_install.sh install
```

## Usage

### Command Line

```bash
# Basic usage (automatically uses .gitignore and .syncignore if present)
pysync source/ destination/

# Specify custom ignore files
pysync source/ destination/ --ignore-files .customignore .npmignore

# Parse ignore files and add as explicit excludes
pysync source/ destination/ --parse-ignore-files

# Enable CVS exclude patterns
pysync source/ destination/ --use-cvs-exclude

# Combine options
pysync source/ destination/ --ignore-files .customignore --parse-ignore-files --use-cvs-exclude

# Remote sync with SSH
pysync source/ user@remote:destination/

# Dry run to see what would be synced
pysync source/ destination/ --dry-run
```

### Python API

```python
from pysync.rsync import make_rsync_command, execute_rsync

# Basic usage (uses .gitignore and .syncignore by default)
cmd = make_rsync_command("source/", "destination/")

# Custom ignore files with explicit parsing
cmd = make_rsync_command(
    source="source/",
    target="destination/",
    ignore_files=['.customignore', '.npmignore'],
    parse_ignore_files=True
)

# With CVS exclude patterns
cmd = make_rsync_command(
    source="source/",
    target="destination/",
    use_cvs_exclude=True
)

# Additional options
cmd = make_rsync_command(
    source="source/",
    target="destination/",
    dry_run=True,
    max_size='10M',
    delete=True,
    exclude=['*.pyc', 'node_modules/']
)

# Execute the command
exit_code = execute_rsync(cmd)
```

## Development

To contribute or modify the package:

```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Clone the repository
git clone https://github.com/colinconwell/PySyncPack.git
cd PySyncPack

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Requirements

- Python 3.8 or higher
- rsync installation
- SSH (for remote syncing)
