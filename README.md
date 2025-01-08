# PySyncPack

An enhanced rsync wrapper with native VCS and .gitignore support, providing both a Python API and a command-line interface.

*Caveat Emptor*: The code in this package was developed and tested by a human, but may still contain bugs. Documentation was written largely by a machine (Claude 3.5 Sonnet), and may contain errors.

## Features

- Native .gitignore / CVS support
- Additional .syncignore support
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
# Basic usage
pysync source/ destination/

# With .gitignore support (default)
pysync source/ destination/

# Disable .gitignore support
pysync source/ destination/ --no-gitignore

# Use custom ignore file
pysync source/ destination/ --ignore-file .syncignore

# Remote sync with SSH
pysync source/ user@remote:destination/

# Dry run to see what would be synced
pysync source/ destination/ --dry-run
```

### Python API

```python
from pysync.rsync import make_rsync_command, execute_rsync

# Generate rsync command
cmd = make_rsync_command(
    source="source/",
    target="destination/",
    dry_run=True,
    ignore_file=".gitignore",
    use_gitignore=True
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
