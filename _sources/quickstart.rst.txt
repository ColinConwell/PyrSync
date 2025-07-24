Quick Start
============

Basic Usage
----------

Command Line Interface
--------------------

The simplest way to use PySync is through its command-line interface:

.. code-block:: bash

    # Sync a local directory
    pysync source/ destination/

    # Sync to a remote server
    pysync source/ user@remote:destination/

By default, PySync will:
- Use `.gitignore` and `.syncignore` if present
- Exclude common development files and directories
- Show progress during transfer

Working with Ignore Files
-----------------------

PySync provides flexible options for handling ignore patterns:

.. code-block:: bash

    # Use a specific ignore file
    pysync source/ dest/ --ignore-files .customignore

    # Use multiple ignore files
    pysync source/ dest/ --ignore-files .npmignore .customignore

    # Preview what patterns would be excluded
    pysync --show-patterns
    pysync --show-patterns --ignore-files .customignore

Testing with Dry Run
------------------

Before performing actual syncs, you can preview what would happen:

.. code-block:: bash

    # Preview what would be synced
    pysync source/ dest/ --dry-run

Python API
---------

PySync can also be used as a Python library:

.. code-block:: python

    from pysync import make_rsync_command, execute_rsync

    # Basic sync
    cmd = make_rsync_command("source/", "destination/")
    execute_rsync(cmd)

    # With custom ignore file
    cmd = make_rsync_command(
        source="source/",
        target="destination/",
        ignore_files=".customignore"
    )

    # Test first, then execute
    execute_rsync(cmd, dry_run=True)  # Preview
    execute_rsync(cmd)  # Actual sync

Common Patterns
-------------

Here are some common usage patterns:

Development Workflow
------------------

.. code-block:: bash

    # Sync project excluding dev files
    pysync project/ backup/ --ignore-files .gitignore

    # Sync with deletion of extraneous files
    pysync source/ dest/ --delete

Remote Backup
------------

.. code-block:: bash

    # Sync to remote server with compression
    pysync -az source/ user@server:backup/

    # Sync excluding large files
    pysync source/ dest/ --max-size=100M

Next Steps
---------

- See :doc:`examples` for more detailed examples
- Check :doc:`api` for full API reference