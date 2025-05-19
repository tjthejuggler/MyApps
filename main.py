#!/usr/bin/env python3
"""
KDE Tray Script Launcher
A simple tray application that allows running scripts from the system tray.
"""
import os
import sys
from ui_manager import TrayApp

def main():
    # Get the absolute path to the icon
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "alien_icon.png")
    
    # Check if the icon exists
    if not os.path.exists(icon_path):
        print(f"Error: Icon not found at {icon_path}")
        sys.exit(1)
    
    # Create and run the tray app
    app = TrayApp(icon_path)
    sys.exit(app.run())

if __name__ == "__main__":
    main()