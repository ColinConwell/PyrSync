# PyrSync: Python + Rsync

An enhanced Python wrapper for [`rsync`](https://rsync.samba.org/), providing both a Python API and a command-line interface.

*Caveat Emptor*: The code in this package was developed and tested by a human, but may still contain bugs. Documentation was written largely by a machine (Claude 3.5 Sonnet), and may contain errors.

## Features

- Smart ignore file handling:
  - Native support for `.gitignore` and `.syncignore`
  - Flexible parsing options for ignore files
  - Pattern preview and extraction capabilities
- Common dev exclusions by default
- Both CLI + Python API interfaces
- SSH support for remote syncing
- Dynamic dry-run control for testing

## Installation

### Using pip (Recommended)

```bash
pip install git+https://github.com/colinconwell/PyrSync.git
```

### Using Poetry

```bash
poetry add git+https://github.com/colinconwell/PyrSync.git
```

### CLI Tool Only

If you only want the command-line tool without installing the Python package:

```bash
curl -O https://raw.githubusercontent.com/colinconwell/PyrSync/main/scripts/cli_install.sh
chmod +x cli_install.sh
./cli_install.sh install
```

## Usage

### Python API

```python
from pysync import make_rsync_command, execute_rsync, get_ignore_patterns

# Basic usage (uses .gitignore and .syncignore by default)
cmd = make_rsync_command("source/", "destination/")

# Use a single ignore file
cmd = make_rsync_command(
    source="source/",
    target="destination/",
    ignore_files=".customignore"  # String for single file
)

# Use multiple ignore files
cmd = make_rsync_command(
    source="source/",
    target="destination/",
    ignore_files=[".customignore", ".npmignore"]  # List for multiple files
)

# Preview patterns from files
patterns = get_ignore_patterns(".customignore", verbose=True)  # Single file
patterns = get_ignore_patterns([".customignore", ".npmignore"], verbose=True)  # Multiple files
patterns = get_ignore_patterns(as_list=True)  # Return as list instead of set

# Parse ignore files and use as explicit excludes
cmd = make_rsync_command(
    source="source/",
    target="destination/",
    ignore_files=".customignore",
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

# Execute commands with dry-run control
cmd = make_rsync_command("source/", "destination/", dry_run=True)
execute_rsync(cmd)  # Runs in dry-run mode as specified
execute_rsync(cmd, dry_run=False)  # Overrides to actual execution
execute_rsync(cmd, dry_run=True)  # Forces dry-run regardless of command setting

# Generate command without dry-run but test first
cmd = make_rsync_command("source/", "destination/", dry_run=False)
execute_rsync(cmd, dry_run=True)  # Test run
execute_rsync(cmd)  # Actual execution
```

### Command Line

```bash
# Basic usage (automatically uses .gitignore and .syncignore if present)
pysync source/ destination/

# Use a single ignore file
pysync source/ destination/ --ignore-files .customignore

# Use multiple ignore files
pysync source/ destination/ --ignore-files .customignore .npmignore

# Preview patterns from a specific ignore file
pysync --show-patterns --ignore-files .customignore

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

## Development

To contribute or modify the package:

```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Clone the repository
git clone https://github.com/colinconwell/PyrSync.git
cd PyrSync

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Requirements

- Python 3.8 or higher
- rsync installation
- SSH (for remote syncing)