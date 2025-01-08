#!/usr/bin/env python3

"""
PySyncPack - Enhanced rsync wrapper with native VCS and .gitignore support
Can be used both as a Python module and as a command-line tool.
"""

import os, sys, subprocess
from pathlib import Path
from typing import Union, List, Optional, Set

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

def get_ignore_patterns(ignore_files: Optional[Union[str, List[str]]] = None, 
                       include_defaults: bool = True,
                       as_list: bool = False,
                       verbose: bool = False) -> Union[List[str], Set[str]]:
    """
    Parse ignore files and return exclusion patterns.
    
    Args:
        ignore_files: Ignore file(s) to parse. Can be a string or list.
                     (default: ['.gitignore', '.syncignore'])
        include_defaults: Whether to include default exclusions (default: True)
        as_list: Return as list instead of set (default: False)
        verbose: Print patterns as they're found (default: False)
    
    Returns:
        Set or List of exclusion patterns
    """
    if ignore_files is None:
        ignore_files = ['.gitignore', '.syncignore']
    elif isinstance(ignore_files, str):
        ignore_files = [ignore_files]
    
    patterns: Set[str] = set()
    
    # Add patterns from ignore files
    for ignore_file in ignore_files:
        if os.path.exists(ignore_file):
            file_patterns = parse_ignore_file(ignore_file)
            if verbose:
                print(f"\nPatterns from {ignore_file}:")
                for pattern in file_patterns:
                    print(f"  {pattern}")
            patterns.update(file_patterns)
    
    # Add default exclusions if requested
    if include_defaults:
        if verbose:
            print("\nDefault exclusion patterns:")
        for key, values in RSYNC_EXCLUSIONS.items():
            values = _fix_exclusions(values, key)
            if verbose:
                for value in values:
                    print(f"  {value}")
            patterns.update(values)
    
    return list(patterns) if as_list else patterns

def _fix_exclusions(exclusions: List[str], exclusion_type: str) -> List[str]:
    """Fix exclusion patterns based on type."""
    fixed = exclusions.copy()
    
    if exclusion_type == 'FILE_TYPES':
        fixed = ['*' + exc if not exc.startswith('*') else exc for exc in fixed]

    if exclusion_type == 'FOLDERS':
        fixed = [exc + '/' if not exc.endswith('/') else exc for exc in fixed]

    return fixed

def make_rsync_command(source: str, target: str, dry_run: bool = True,
                      ignore_files: Optional[Union[str, List[str]]] = None,
                      parse_ignore_files: bool = False,
                      **kwargs) -> Union[str, List[str]]:
    """
    Create rsync command with enhanced exclusion handling and VCS support.
    
    Args:
        source: source path
        target: target path
        dry_run: Whether to do a dry run
        ignore_files: Ignore file(s) to use. Can be a string or list.
                     (default: ['.gitignore', '.syncignore'])
        parse_ignore_files: If True, parse ignore files and add as --exclude, else use filter
        **kwargs: Additional arguments including:
            - max_size: Maximum file size
            - delete: Whether to delete extraneous files
            - as_list: Return command as list instead of string
            - exclude: Additional exclusion patterns
            - use_cvs_exclude: Use CVS exclude patterns (default: False)
    """
    # Build command
    rsync_cmd = ["rsync", "-avhP"]
    
    # Handle CVS exclude
    if kwargs.pop('use_cvs_exclude', False):
        rsync_cmd.append("--cvs-exclude")
    
    if max_size := kwargs.pop('max_size', None):
        rsync_cmd.append(f'--max-size={max_size}')
    
    if dry_run:
        rsync_cmd.append('--dry-run')
    
    # Handle ignore files
    if ignore_files is None:
        ignore_files = ['.gitignore', '.syncignore']
    elif isinstance(ignore_files, str):
        ignore_files = [ignore_files]
    
    # Track all exclusion patterns to avoid duplicates
    exclusion_patterns: Set[str] = set()
    
    # Add patterns from ignore files
    if parse_ignore_files:
        # Get all patterns from ignore files and defaults
        patterns = get_ignore_patterns(ignore_files, include_defaults=False)
        for pattern in patterns:
            if pattern not in exclusion_patterns:
                rsync_cmd.append(f"--exclude='{pattern}'")
                exclusion_patterns.add(pattern)
    else:
        # Use filter mechanism
        for ignore_file in ignore_files:
            if os.path.exists(ignore_file):
                rsync_cmd.append(f"--filter=':- {ignore_file}'")
    
    # Add default exclusions
    for key, values in RSYNC_EXCLUSIONS.items():
        values = _fix_exclusions(values, key)
        for value in values:
            if value not in exclusion_patterns:
                rsync_cmd.append(f"--exclude='{value}'")
                exclusion_patterns.add(value)
    
    # Add custom exclusions
    exclusions = kwargs.pop('exclude', None)
    if exclusions:
        if isinstance(exclusions, list):
            for excl in exclusions:
                if excl not in exclusion_patterns:
                    rsync_cmd.append(f"--exclude='{excl}'")
                    exclusion_patterns.add(excl)
        elif isinstance(exclusions, dict):
            for values in exclusions.values():
                if isinstance(values, str):
                    values = [values]
                for value in values:
                    if value not in exclusion_patterns:
                        rsync_cmd.append(f"--exclude='{value}'")
                        exclusion_patterns.add(value)
    
    # Add SSH and paths
    rsync_cmd.extend(['-e', 'ssh', source, target])
    
    if kwargs.pop('delete', False):
        rsync_cmd.append('--delete')
    
    return rsync_cmd if kwargs.pop('as_list', False) else ' '.join(rsync_cmd)

def execute_rsync(command: Union[str, List[str]], verbose: bool = True, 
                  dry_run: Optional[bool] = None) -> int:
    """
    Execute rsync command and return exit code.
    
    Args:
        command: The rsync command as string or list
        verbose: Whether to print the command before execution
        dry_run: Override dry-run setting. If None, uses the setting from command.
                If True/False, adds/removes --dry-run flag regardless of command setting.
    """
    if isinstance(command, list):
        cmd_list = command
    else:
        cmd_list = command.split()
    
    # Handle dry-run override if specified
    if dry_run is not None:
        # Remove existing dry-run flag if present
        cmd_list = [arg for arg in cmd_list if arg != '--dry-run']
        # Add dry-run flag if requested
        if dry_run:
            cmd_list.insert(1, '--dry-run')  # Insert after 'rsync'
    
    # Convert back to string
    final_cmd = ' '.join(cmd_list)
    
    if verbose:
        print(f"Executing: {final_cmd}")
    
    return subprocess.call(final_cmd, shell=True)

def cli_main():
    """Entry point for command-line usage."""
    from argparse import ArgumentParser
    
    parser = ArgumentParser(
        description='Enhanced rsync with native VCS and .gitignore support',
        usage='%(prog)s [rsync_options] source destination [options]'
    )
    parser.add_argument('--ignore-files', nargs='+', 
                       help='List of ignore files to use (default: .gitignore .syncignore)')
    parser.add_argument('--parse-ignore-files', action='store_true',
                       help='Parse ignore files and add as --exclude instead of using filter')
    parser.add_argument('--use-cvs-exclude', action='store_true',
                       help='Use CVS exclude patterns')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show command without executing')
    parser.add_argument('--show-patterns', action='store_true',
                       help='Show patterns that would be excluded')
    parser.add_argument('--version', action='version', 
                       version=f'pysync {__version__}')
    
    # Parse known args to get our custom options while preserving rsync args
    known_args, rsync_args = parser.parse_known_args()
    
    try:
        # If just showing patterns, do that and exit
        if known_args.show_patterns:
            get_ignore_patterns(known_args.ignore_files, verbose=True)
            return 0
        
        paths = [arg for arg in rsync_args if not arg.startswith('-')]
        if len(paths) != 2:
            raise ValueError("Exactly two paths (source and destination) are required")
            
        cmd = make_rsync_command(
            source=paths[0],
            target=paths[1],
            dry_run=known_args.dry_run,
            ignore_files=known_args.ignore_files,
            parse_ignore_files=known_args.parse_ignore_files,
            use_cvs_exclude=known_args.use_cvs_exclude
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