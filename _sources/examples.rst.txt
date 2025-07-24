Examples and Use Cases
====================

This section provides detailed examples and real-world use cases for PySync.

Project Backup Workflow
----------------------

Here's a complete workflow for backing up a Python project:

.. code-block:: python

    from pysync import make_rsync_command, execute_rsync, get_ignore_patterns

    # First, let's see what would be excluded
    patterns = get_ignore_patterns(
        ignore_files=['.gitignore', '.syncignore'],
        verbose=True
    )

    # Create the sync command
    cmd = make_rsync_command(
        source="my_project/",
        target="backups/my_project/",
        ignore_files=['.gitignore', '.syncignore'],
        max_size='100M',  # Skip large files
        delete=True       # Remove extraneous files
    )

    # Test first
    execute_rsync(cmd, dry_run=True)

    # If everything looks good, execute
    execute_rsync(cmd, dry_run=False)

Remote Development Setup
-----------------------

Syncing a development environment to a remote server:

.. code-block:: python

    def sync_to_remote(local_path, remote_host, remote_path, dry_run=True):
        """Sync local development to remote server."""
        cmd = make_rsync_command(
            source=f"{local_path}/",
            target=f"{remote_host}:{remote_path}/",
            ignore_files=".gitignore",
            parse_ignore_files=True,  # Use explicit excludes
            dry_run=dry_run
        )
        return execute_rsync(cmd)

    # Usage
    sync_to_remote(
        local_path="~/projects/webapp",
        remote_host="user@dev-server",
        remote_path="/var/www/webapp",
        dry_run=True
    )

Custom Ignore Patterns
---------------------

Example of combining different ignore patterns:

.. code-block:: python

    # Custom exclusions
    custom_excludes = {
        'FOLDERS': ['node_modules', 'venv', '.env'],
        'FILE_TYPES': ['*.log', '*.tmp', '*.swp'],
        'FILE_NAMES': ['secret.key', 'config.local']
    }

    cmd = make_rsync_command(
        source="project/",
        target="backup/",
        ignore_files=".gitignore",
        exclude=custom_excludes
    )

Command Line Examples
--------------------

Common command-line usage patterns:

Development Sync
---------------

.. code-block:: bash

    # Sync excluding development artifacts
    pysync project/ backup/ --ignore-files .gitignore --parse-ignore-files

    # Sync with size limit and progress
    pysync -P --max-size=50M source/ dest/

    # Sync deleting extraneous files
    pysync --delete source/ dest/

Remote Deployment
----------------

.. code-block:: bash

    # Deploy to staging
    pysync -az --delete project/ user@staging:/var/www/app/

    # Deploy to production with dry-run
    pysync -az --delete --dry-run project/ user@prod:/var/www/app/

Backup Scenarios
---------------

.. code-block:: bash

    # Daily backup with timestamp
    DATE=$(date +%Y%m%d)
    pysync project/ backups/project_$DATE/

    # Incremental backup
    pysync -a --delete project/ backups/latest/

Advanced Usage
-------------

Using PySync in Scripts
----------------------

Here's an example of using PySync in a backup script:

.. code-block:: python

    import os
    from datetime import datetime
    from pysync import make_rsync_command, execute_rsync

    def create_backup(source_dir, backup_base, max_backups=5):
        """Create a timestamped backup and maintain a limited number of backups."""
        
        # Create timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = os.path.join(backup_base, f"backup_{timestamp}")
        
        # Create sync command
        cmd = make_rsync_command(
            source=source_dir,
            target=backup_dir,
            ignore_files=".backupignore",
            parse_ignore_files=True,
            dry_run=False
        )
        
        # Execute backup
        result = execute_rsync(cmd)
        
        if result == 0:
            print(f"Backup created at: {backup_dir}")
            
            # Cleanup old backups
            backups = sorted([
                d for d in os.listdir(backup_base)
                if d.startswith("backup_")
            ])
            
            if len(backups) > max_backups:
                for old_backup in backups[:-max_backups]:
                    old_path = os.path.join(backup_base, old_backup)
                    print(f"Removing old backup: {old_path}")
                    os.system(f"rm -rf {old_path}")
        
        return result

    # Usage
    create_backup(
        source_dir="~/projects/important_project",
        backup_base="~/backups",
        max_backups=5
    )

Error Handling
-------------

Example of robust error handling:

.. code-block:: python

    def safe_sync(source, target, ignore_files=None, max_retries=3):
        """Perform sync with error handling and retries."""
        for attempt in range(max_retries):
            try:
                cmd = make_rsync_command(
                    source=source,
                    target=target,
                    ignore_files=ignore_files,
                    dry_run=False
                )
                
                result = execute_rsync(cmd)
                
                if result == 0:
                    print("Sync successful!")
                    return True
                else:
                    print(f"Sync failed with exit code: {result}")
                    
            except Exception as e:
                print(f"Error during sync (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    print("Retrying...")
                    continue
                
        return False

    # Usage
    success = safe_sync(
        source="project/",
        target="backup/",
        ignore_files=".syncignore",
        max_retries=3
    ) 