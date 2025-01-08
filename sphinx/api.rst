API Reference
=============

Core Functions
--------------

.. automodule:: pysync
   :members:
   :undoc-members:
   :show-inheritance:

Command Line Interface
----------------------

The command-line interface provides the following options:

.. code-block:: text

    usage: pysync [rsync_options] source destination [options]

    options:
      --ignore-files IGNORE_FILES [IGNORE_FILES ...]
                            List of ignore files to use (default: .gitignore .syncignore)
      --parse-ignore-files  Parse ignore files and add as --exclude instead of using filter
      --use-cvs-exclude    Use CVS exclude patterns
      --dry-run            Show command without executing
      --show-patterns      Show patterns that would be excluded
      --version            Show program's version number and exit

Default Exclusions
------------------

The following patterns are excluded by default:

Folders:
    - .ipynb_checkpoints/
    - __pycache__/
    - *.git/
    - .vscode/

File Types:
    - *_rsync.sh
    - *.sh
    - *.git*
    - *.pt

These defaults can be overridden or supplemented using ignore files or command-line options. 