Installation
============

PySync can be installed in several ways, depending on your needs and workflow.

Prerequisites
-------------

Before installing PySync, ensure you have:

- Python 3.10 or higher
- rsync installation
- SSH (optional, for remote syncing)

To check your Python version:

.. code-block:: bash

    python --version

To check if rsync is installed:

.. code-block:: bash

    rsync --version

Installation Methods
--------------------

Using pip (Recommended)
^^^^^^^^^^^^^^^^^^^^^^^

The simplest way to install PySync is directly from GitHub using pip:

.. code-block:: bash

    pip install git+https://github.com/colinconwell/PySync.git

Using Poetry
^^^^^^^^^^^^

If you're using Poetry for dependency management:

.. code-block:: bash

    poetry add git+https://github.com/colinconwell/PySync.git

CLI Tool Only
^^^^^^^^^^^^^

If you only want the command-line tool without installing the Python package:

.. code-block:: bash

    curl -O https://raw.githubusercontent.com/colinconwell/PySync/main/scripts/cli_install.sh
    chmod +x cli_install.sh
    ./cli_install.sh install

Development Installation
------------------------

For development or contributing:

.. code-block:: bash

    # Clone the repository
    git clone https://github.com/colinconwell/PySync.git
    cd PySync

    # Using Poetry (recommended)
    poetry install

    # Or using pip
    pip install -e .

With Documentation Dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To build the documentation locally:

.. code-block:: bash

    # Using Poetry
    poetry install --with docs

    # Using pip
    pip install -e ".[docs]"

Verifying Installation
----------------------

After installation, verify that PySync is working:

.. code-block:: bash

    # Check CLI tool
    pysync --version

    # Check Python package
    python -c "from pysync import make_rsync_command; print('PySync is installed!')"