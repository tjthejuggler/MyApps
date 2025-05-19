# KDE Tray Script Launcher

A simple KDE tray application that allows you to manage and run scripts directly from the system tray.

## Features

- System tray icon (displayed at 2x size) with context menu for quick script access
- Left-click on the tray icon opens a management window
- Right-click on the tray icon shows a menu with all configured scripts
- Add, remove, and manage scripts through a simple interface
- Reorder scripts by moving them up or down in the list
- Automatically starts when you log in to your KDE session
- Run scripts directly from the tray menu

## Requirements

- Python 3.6+
- PyQt5

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python main.py
```

### Adding Scripts

1. Left-click on the tray icon to open the management window
2. Enter a name for your script
3. Enter the path to the script or use the "Browse..." button to select it
4. Click "Add Script"

### Running Scripts

1. Right-click on the tray icon to open the context menu
2. Click on the script name you want to run

### Removing Scripts

1. Left-click on the tray icon to open the management window
2. Select the script you want to remove from the list
3. Click "Remove Selected"

### Reordering Scripts

1. Left-click on the tray icon to open the management window
2. Select the script you want to move from the list
3. Click "Move Up" or "Move Down" to change its position in the list
4. The order in the management window will be the same as in the right-click menu

## Supported Script Types

The application attempts to run scripts based on their file extension:

- `.py` files are run with `python3`
- `.sh` files are run with `bash`
- Other files are executed directly

## Data Storage

Script configurations are stored in a JSON file (`script_items.json`) in the same directory as the application.

## Autostart with KDE

The application is already configured to start automatically when you log in to your KDE session. The autostart configuration is stored in:

```
~/.config/autostart/kde-script-launcher.desktop
```

If you move the application to a different location, you'll need to update this file with the new paths.