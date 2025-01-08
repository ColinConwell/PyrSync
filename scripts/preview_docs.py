#!/usr/bin/env python3

"""
Preview Sphinx documentation locally using Python's HTTP server.
Run this script from the project root directory.
"""

import os
import sys
import http.server
import socketserver
import subprocess
import webbrowser
from pathlib import Path

def build_docs():
    """Build Sphinx documentation."""
    sphinx_dir = Path("sphinx")
    build_dir = sphinx_dir / "_build" / "html"
    
    # Ensure we're in the project root
    if not sphinx_dir.exists():
        print("Error: 'sphinx' directory not found. Run this script from the project root.")
        sys.exit(1)
    
    print("Building documentation...")
    try:
        subprocess.run(["make", "html"], cwd=sphinx_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error building documentation: {e}")
        sys.exit(1)
    
    return build_dir

def serve_docs(build_dir, port=8000):
    """Serve documentation using Python's HTTP server."""
    os.chdir(build_dir)
    
    handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            url = f"http://localhost:{port}"
            print(f"\nServing documentation at {url}")
            print("Press Ctrl+C to stop the server")
            
            # Open browser
            webbrowser.open(url)
            
            # Start server
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"\nError: Port {port} is already in use. Try a different port:")
            print(f"python {sys.argv[0]} --port <port_number>")
            sys.exit(1)
        raise

def main():
    """Main function."""
    # Parse command line arguments
    port = 8000
    if len(sys.argv) > 1:
        if sys.argv[1] == "--port" and len(sys.argv) > 2:
            try:
                port = int(sys.argv[2])
            except ValueError:
                print("Error: Port must be a number")
                sys.exit(1)
    
    # Build and serve docs
    build_dir = build_docs()
    serve_docs(build_dir, port)

if __name__ == "__main__":
    main() 