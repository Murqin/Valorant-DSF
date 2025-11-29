"""
Valorant DSF Launcher
---------------------
This script serves as the entry point for the application.
It allows the user to choose between the Desktop App (Native) and the Web Server (LAN).
"""

import os
import sys
import subprocess

def main():
    """
    Main entry point. Displays a CLI menu to select the application mode.
    """
    print("Valorant DSF Launcher")
    print("----------------")
    print("1. Desktop App (Native, Auto-Login)")
    print("2. Web Server (LAN, Paste-Login)")
    print("----------------")
    
    choice = input("Select mode (1/2): ").strip()
    
    python_exe = sys.executable
    
    if choice == "1":
        print("Starting Desktop App...")
        # Run main.py inside apps/desktop
        app_dir = os.path.join("apps", "desktop")
        subprocess.run([python_exe, "main.py"], cwd=app_dir)
        
    elif choice == "2":
        print("Starting Web Server...")
        # Run main.py inside apps/web
        app_dir = os.path.join("apps", "web")
        subprocess.run([python_exe, "main.py"], cwd=app_dir)
        
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
