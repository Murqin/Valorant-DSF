# Copyright (c) 2025 Icarus Murqin
# Licensed under the MIT License. See LICENSE file for details.

"""
Build Script for Valorant-DSF Desktop Application.

This script utilizes PyInstaller to bundle the Python application into a standalone
executable (.exe) file for Windows. It handles the inclusion of static assets,
HTML templates, SSL certificates, and correct path resolutions for the monorepo structure.

Usage:
    Execute this script from the project root directory using the virtual environment:
    $ python build_desktop.py
"""

import PyInstaller.__main__
import os
import sys

def build_executable():
    """
    Configures and runs PyInstaller with the necessary arguments to build the Desktop App.
    
    The function performs the following steps:
    1. Identifies absolute paths for assets and entry points.
    2. Configures data bundling (HTML, CSS, SSL Certs).
    3. Sets up import paths to ensure 'core' modules are found.
    4. Executes the build process.
    """
    
    # 1. Setup Base Paths
    # We use abspath to ensure PyInstaller finds files regardless of where the command is run.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the application icon
    icon_path = os.path.join(base_dir, 'assets', 'icon.ico')
    
    # Path to the main entry point of the Desktop Application
    entry_point = os.path.join(base_dir, 'apps', 'desktop', 'main.py')

    print(f"--- Starting Build Process for ValoStore ---")
    print(f"Base Directory: {base_dir}")
    print(f"Entry Point:    {entry_point}")

    # 2. Configure Data Bundling (--add-data)
    # Format for Windows: "source_path;destination_folder"
    # We need to bundle:
    # - The Icon (for runtime usage)
    # - HTML Templates (apps/desktop/templates -> templates)
    # - CSS/JS Static files (apps/desktop/static -> static)
    # - SSL Certificates (cert.pem/key.pem -> root)
    added_data = [
        f'{icon_path};assets',
        'apps/desktop/templates;templates',
        'apps/desktop/static;static',
        'cert.pem;.',
        'key.pem;.'
    ]

    # 3. Construct PyInstaller Arguments
    args = [
        entry_point,                        # The script to run
        '--name=Valorant-DSF_v1.0.0',       # Name of the output .exe
        '--onefile',                        # Bundle everything into a single file
        '--noconsole',                      # Do not show a terminal window (GUI mode)
        f'--icon={icon_path}',              # Set the .exe file icon
        '--paths=.',                        # CRITICAL: Add root dir to python path so 'core' module is found
        '--collect-all=tls_client',         # Explicitly collect tls_client dependencies (avoids DLL errors)
        '--clean',                          # Clean PyInstaller cache before building
    ]

    # Append data arguments dynamically
    for data in added_data:
        args.append(f'--add-data={data}')

    # 4. Execute Build
    print(f"PyInstaller Arguments: {args}")
    
    try:
        PyInstaller.__main__.run(args)
        print("\n>>> Build Successful! Check the 'dist' folder.")
    except Exception as e:
        print(f"\n>>> Build Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_executable()