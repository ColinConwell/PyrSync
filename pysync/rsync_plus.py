#!/usr/bin/env python3

"""
PySyncPack - Enhanced rsync wrapper with native VCS and .gitignore support
Can be used both as a Python module and as a command-line tool.
"""

import os, sys, subprocess
from pathlib import Path
from typing import Union, List, Optional

__version__ = '0.1.0'

RSYNC_EXCLUSIONS = {
    'FOLDERS': ['.ipynb_checkpoints', '__pycache__', '.vscode', '*.git'],
    'FILE_TYPES': ["*_rsync.sh", "*.sh", "*.git*", '*.pt'],
    'FILE_NAMES': [],
}

def parse_ignore_file(file_path: Union[str, Path]) -> List[str]:
    """Parse .syncignore or .gitignore file and return list of patterns."""
    patterns = []
    if not os.path.exists(file_path):
        return patterns
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                patterns.append(line)
    return patterns

def _fix_exclusions(exclusions: List[str], exclusion_type: str) -> List[str]:
    """Fix exclusion patterns based on type."""
    fixed = exclusions.copy()
    
    if exclusion_type == 'FILE_TYPES':
        fixed = ['*' + exc if not exc.startswith('*') else exc for exc in fixed]

    if exclusion_type == 'FOLDERS':
        fixed = [exc + '/' if not exc.endswith('/') else exc for exc in fixed]

    return fixed

def make_rsync_command(source: str, target: str, dry_run: bool = True,
                      ignore_file: Optional[str] = None,
                      use_gitignore: bool = True,
                      use_cvs_exclude: bool = True,
                      **kwargs) -> Union[str, List[str]]:
    """
    Create rsync command with enhanced exclusion handling and VCS support.
    
    Args:
        source: source path
        target: target path
        dry_run: Whether to do a dry run
        ignore_file: Path to .syncignore or .gitignore file
        use_gitignore: Use native .gitignore support (default: True)
        use_cvs_exclude: Use native CVS exclude (default: True)
        **kwargs: Additional arguments including:
            - max_size: Maximum file size
            - delete: Whether to delete extraneous files
            - as_list: Return command as list instead of string
            - exclude: Additional exclusion patterns
    """
    # Build command
    rsync_cmd = ["rsync", "-avhP"]
    
    # Add native VCS ignore support
    if use_gitignore:
        rsync_cmd.append("--filter=':- .gitignore'")
    if use_cvs_exclude:
        rsync_cmd.append("--cvs-exclude")
    
    if max_size := kwargs.pop('max_size', None):
        rsync_cmd.append(f'--max-size={max_size}')
    
    if dry_run:
        rsync_cmd.append('--dry-run')
    
    # Handle ignore file
    if ignore_file and os.path.exists(ignore_file):
        rsync_cmd.append(f"--filter=':- {ignore_file}'")
    
    # Add default exclusions
    for key, values in RSYNC_EXCLUSIONS.items():
        values = _fix_exclusions(values, key)
        for value in values:
            rsync_cmd.append(f"--exclude='{value}'")
    
    # Add custom exclusions
    exclusions = kwargs.pop('exclude', None)
    if exclusions:
        if isinstance(exclusions, list):
            for excl in exclusions:
                rsync_cmd.append(f"--exclude='{excl}'")
        elif isinstance(exclusions, dict):
            for values in exclusions.values():
                if isinstance(values, str):
                    values = [values]
                for value in values:
                    rsync_cmd.append(f"--exclude='{value}'")
    
    # Add SSH and paths
    rsync_cmd.extend(['-e', 'ssh', source, target])
    
    if kwargs.pop('delete', False):
        rsync_cmd.append('--delete')
    
    return rsync_cmd if kwargs.pop('as_list', False) else ' '.join(rsync_cmd)

def execute_rsync(command: Union[str, List[str]], verbose: bool = True) -> int:
    """Execute rsync command and return exit code."""
    if isinstance(command, list):
        command = ' '.join(command)
    
    if verbose:
        print(f"Executing: {command}")
    
    return subprocess.call(command, shell=True)

def cli_main():
    """Entry point for command-line usage."""
    from argparse import ArgumentParser
    
    parser = ArgumentParser(
        description='Enhanced rsync with native VCS and .gitignore support',
        usage='%(prog)s [rsync_options] source destination [--ignore-file file]'
    )
    parser.add_argument('--ignore-file', help='Path to .syncignore or .gitignore file')
    parser.add_argument('--no-gitignore', action='store_true', 
                       help='Disable native .gitignore support')
    parser.add_argument('--no-cvs-exclude', action='store_true',
                       help='Disable native CVS exclude')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show command without executing')
    parser.add_argument('--version', action='version', 
                       version=f'pysync {__version__}')
    
    # Parse known args to get our custom options while preserving rsync args
    known_args, rsync_args = parser.parse_known_args()
    
    try:
        paths = [arg for arg in rsync_args if not arg.startswith('-')]
        if len(paths) != 2:
            raise ValueError("Exactly two paths (source and destination) are required")
            
        cmd = make_rsync_command(
            source=paths[0],
            target=paths[1],
            dry_run=known_args.dry_run,
            ignore_file=known_args.ignore_file,
            use_gitignore=not known_args.no_gitignore,
            use_cvs_exclude=not known_args.no_cvs_exclude
        )
        
        if known_args.dry_run:
            print(' '.join(cmd))
            return 0
            
        return execute_rsync(cmd)
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    exit(cli_main()) 