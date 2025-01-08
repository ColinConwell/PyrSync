Welcome to PySync's documentation!
==================================

PySyncPack is an enhanced rsync wrapper providing both a Python API and command-line interface, with smart handling of ignore files and generally easier exclusion management.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api
   examples

Features
--------

- Smart ignore file handling:
  - Native support for `.gitignore` and `.syncignore`
  - Flexible parsing options for ignore files
  - Pattern preview and extraction capabilities
- Common dev exclusions by default
- Both CLI + Python API interfaces
- SSH support for remote syncing
- Dynamic dry-run control for testing

Quick Install
-------------

Using pip:

.. code-block:: bash

    pip install git+https://github.com/colinconwell/PySync.git

Using Poetry:

.. code-block:: bash

    poetry add git+https://github.com/colinconwell/PySync.git

Quick Usage
-----------

Command Line:

.. code-block:: bash

    # Basic usage
    pysync source/ destination/

    # With custom ignore file
    pysync source/ destination/ --ignore-files .customignore

Python API:

.. code-block:: python

    from pysync import make_rsync_command, execute_rsync

    # Basic usage
    cmd = make_rsync_command("source/", "destination/")
    execute_rsync(cmd)

    # With custom ignore file
    cmd = make_rsync_command(
        source="source/",
        target="destination/",
        ignore_files=".customignore"
    )
    execute_rsync(cmd)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 