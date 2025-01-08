#!/bin/bash

INSTALL_PATH="/usr/local/bin/pysync"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
SOURCE_SCRIPT="$PARENT_DIR/pysync/rsync.py"

install_tool() {
    echo "Installing pysync..."
    
    # Check if source file exists
    if [ ! -f "$SOURCE_SCRIPT" ]; then
        echo "✗ Source file rsync.py not found at $SOURCE_SCRIPT"
        exit 1
    fi
    
    # Check if rsync is installed
    if ! command -v rsync >/dev/null 2>&1; then
        echo "✗ rsync is not installed. Please install rsync first."
        exit 1
    fi
    
    # Check if Python 3 is installed
    if ! command -v python3 >/dev/null 2>&1; then
        echo "✗ Python 3 is not installed. Please install Python 3 first."
        exit 1
    fi
    
    # Install the CLI tool
    if [ "$EUID" -ne 0 ]; then 
        echo "Requesting sudo privileges to install to $INSTALL_PATH"
        sudo cp "$SOURCE_SCRIPT" "$INSTALL_PATH"
        sudo chmod +x "$INSTALL_PATH"
    else
        cp "$SOURCE_SCRIPT" "$INSTALL_PATH"
        chmod +x "$INSTALL_PATH"
    fi
    
    if [ $? -eq 0 ]; then
        echo "✓ CLI installation successful. You can now use 'pysync' from anywhere."
        echo
        echo "Examples:"
        echo "  pysync source/ dest/"
        echo "  pysync -avzhP source/ user@remote:dest/"
        echo "  pysync source/ dest/ --ignore-file .gitignore"
        echo
        echo "For Python package installation, use:"
        echo "  pip install ."
    else
        echo "✗ Installation failed. Please check permissions and try again."
        exit 1
    fi
}

uninstall_tool() {
    echo "Uninstalling pysync CLI tool..."
    
    if [ ! -f "$INSTALL_PATH" ]; then
        echo "✗ pysync is not installed in $INSTALL_PATH"
        exit 1
    fi
    
    if [ "$EUID" -ne 0 ]; then
        echo "Requesting sudo privileges to remove from $INSTALL_PATH"
        sudo rm "$INSTALL_PATH"
    else
        rm "$INSTALL_PATH"
    fi
    
    if [ $? -eq 0 ]; then
        echo "✓ CLI uninstallation successful"
        echo "Note: Python package can be uninstalled with: pip uninstall pysync"
    else
        echo "✗ Uninstallation failed. Please check permissions and try again."
        exit 1
    fi
}

print_version() {
    if [ -f "$SOURCE_SCRIPT" ]; then
        VERSION=$(grep "__version__" "$SOURCE_SCRIPT" | cut -d"'" -f2)
        echo "pysync version $VERSION"
    else
        echo "Cannot determine version - source file not found"
    fi
}

case "$1" in
    "install")
        install_tool
        ;;
    "uninstall")
        uninstall_tool
        ;;
    "version")
        print_version
        ;;
    *)
        echo "Usage: $0 {install|uninstall|version}"
        echo
        echo "Commands:"
        echo "  install    Install pysync CLI tool to /usr/local/bin"
        echo "  uninstall  Remove pysync CLI tool from /usr/local/bin"
        echo "  version    Show version information"
        echo
        echo "Source file: $SOURCE_SCRIPT"
        echo "Install location: $INSTALL_PATH"
        exit 1
        ;;
esac

exit 0