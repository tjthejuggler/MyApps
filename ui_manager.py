import os
import subprocess
from typing import Dict, List, Callable

from PyQt5.QtWidgets import (
    QApplication, QSystemTrayIcon, QMenu, QAction, QMainWindow,
    QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QListWidget,
    QListWidgetItem, QLabel, QLineEdit, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

from data_manager import DataManager

class ItemManagerWindow(QMainWindow):
    """Window for managing script items (add/remove)"""
    
    def __init__(self, data_manager: DataManager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.setWindowTitle("Script Manager")
        self.setMinimumSize(500, 400)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create list widget to display items
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)
        main_layout.addWidget(QLabel("Configured Scripts:"))
        main_layout.addWidget(self.list_widget)
        
        # Create form for adding new items
        form_layout = QVBoxLayout()
        
        # Name input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)
        form_layout.addLayout(name_layout)
        
        # Script path input
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("Script Path:"))
        self.path_input = QLineEdit()
        path_layout.addWidget(self.path_input)
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse_script)
        path_layout.addWidget(self.browse_button)
        form_layout.addLayout(path_layout)
        
        # Add button
        self.add_button = QPushButton("Add Script")
        self.add_button.clicked.connect(self.add_item)
        form_layout.addWidget(self.add_button)
        
        main_layout.addLayout(form_layout)
        
        # Buttons for managing items
        buttons_layout = QHBoxLayout()
        
        # Remove button
        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.clicked.connect(self.remove_item)
        buttons_layout.addWidget(self.remove_button)
        
        # Move Up button
        self.move_up_button = QPushButton("Move Up")
        self.move_up_button.clicked.connect(self.move_item_up)
        buttons_layout.addWidget(self.move_up_button)
        
        # Move Down button
        self.move_down_button = QPushButton("Move Down")
        self.move_down_button.clicked.connect(self.move_item_down)
        buttons_layout.addWidget(self.move_down_button)
        
        main_layout.addLayout(buttons_layout)
        
        # Refresh the list
        self.refresh_items()
    
    def browse_script(self):
        """Open file dialog to select a script"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Script", "", "All Files (*)"
        )
        if file_path:
            self.path_input.setText(file_path)
    
    def add_item(self):
        """Add a new script item"""
        name = self.name_input.text().strip()
        script_path = self.path_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter a name for the script.")
            return
            
        if not script_path:
            QMessageBox.warning(self, "Input Error", "Please enter a script path.")
            return
            
        if not os.path.exists(script_path):
            result = QMessageBox.question(
                self, 
                "Path Warning", 
                f"The script path '{script_path}' does not exist. Add anyway?",
                QMessageBox.Yes | QMessageBox.No
            )
            if result == QMessageBox.No:
                return
        
        success = self.data_manager.add_item(name, script_path)
        if success:
            self.name_input.clear()
            self.path_input.clear()
            self.refresh_items()
        else:
            QMessageBox.warning(self, "Error", "Failed to add the script.")
    
    def remove_item(self):
        """Remove the selected script item"""
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Selection", "Please select a script to remove.")
            return
            
        selected_item = selected_items[0]
        name = selected_item.text().split(" (")[0]  # Extract name from display text
        
        result = QMessageBox.question(
            self, 
            "Confirm Removal", 
            f"Are you sure you want to remove '{name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if result == QMessageBox.Yes:
            success = self.data_manager.remove_item(name)
            if success:
                self.refresh_items()
            else:
                QMessageBox.warning(self, "Error", "Failed to remove the script.")
    
    def move_item_up(self):
        """Move the selected item up in the list"""
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Selection", "Please select a script to move.")
            return
            
        selected_item = selected_items[0]
        name = selected_item.text().split(" (")[0]  # Extract name from display text
        
        success = self.data_manager.move_item_up(name)
        if success:
            self.refresh_items()
            
            # Re-select the moved item
            index = self.data_manager.get_item_index(name)
            if index is not None:
                self.list_widget.setCurrentRow(index)
        else:
            QMessageBox.information(self, "Move Item", "Cannot move item up further.")
    
    def move_item_down(self):
        """Move the selected item down in the list"""
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Selection", "Please select a script to move.")
            return
            
        selected_item = selected_items[0]
        name = selected_item.text().split(" (")[0]  # Extract name from display text
        
        success = self.data_manager.move_item_down(name)
        if success:
            self.refresh_items()
            
            # Re-select the moved item
            index = self.data_manager.get_item_index(name)
            if index is not None:
                self.list_widget.setCurrentRow(index)
        else:
            QMessageBox.information(self, "Move Item", "Cannot move item down further.")
    
    def refresh_items(self):
        """Refresh the list of items"""
        self.list_widget.clear()
        items = self.data_manager.get_all_items()
        
        for name, path in items:
            display_text = f"{name} ({path})"
            item = QListWidgetItem(display_text)
            self.list_widget.addItem(item)


class TrayApp:
    """Main application class for the system tray app"""
    
    def __init__(self, icon_path: str):
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)  # Keep running when windows are closed
        
        # Initialize data manager
        self.data_manager = DataManager()
        
        # Load and resize the icon for use throughout the application
        self.pixmap = QPixmap(icon_path)
        original_size = self.pixmap.size()
        self.resized_pixmap = self.pixmap.scaled(original_size.width() * 2, original_size.height() * 2)
        self.app_icon = QIcon(self.resized_pixmap)
        
        # Set application icon
        self.app.setWindowIcon(self.app_icon)
        
        # Create system tray icon with a larger icon
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(self.app_icon)
        self.tray_icon.setToolTip("Script Launcher")
        
        # Create manager window (initially hidden)
        self.manager_window = ItemManagerWindow(self.data_manager)
        self.manager_window.setWindowIcon(self.app_icon)  # Set window icon
        
        # Connect tray icon signals
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
        # Create tray menu
        self.tray_menu = QMenu()
        self.update_tray_menu()
        
        # Set the menu for the tray icon
        self.tray_icon.setContextMenu(self.tray_menu)
        
        # Show the tray icon
        self.tray_icon.show()
    
    def tray_icon_activated(self, reason):
        """Handle tray icon activation (click)"""
        if reason == QSystemTrayIcon.Trigger:  # Left click
            self.show_manager_window()
    
    def show_manager_window(self):
        """Show the item manager window"""
        self.manager_window.refresh_items()  # Refresh before showing
        self.manager_window.show()
        self.manager_window.raise_()
        self.manager_window.activateWindow()
    
    def update_tray_menu(self):
        """Update the tray icon context menu with current items"""
        self.tray_menu.clear()
        
        # Add script items
        items = self.data_manager.get_all_items()
        for name, script_path in items:
            action = QAction(name, self.tray_menu)
            action.triggered.connect(lambda checked=False, path=script_path: self.run_script(path))
            self.tray_menu.addAction(action)
        
        if items:
            self.tray_menu.addSeparator()
        
        # Add manage action
        manage_action = QAction("Manage Scripts", self.tray_menu)
        manage_action.triggered.connect(self.show_manager_window)
        self.tray_menu.addAction(manage_action)
        
        # Add quit action
        quit_action = QAction("Quit", self.tray_menu)
        quit_action.triggered.connect(self.app.quit)
        self.tray_menu.addAction(quit_action)
    
    def run_script(self, script_path: str):
        """Run the specified script"""
        try:
            # Check if the script exists
            if not os.path.exists(script_path):
                QMessageBox.warning(
                    None, 
                    "Error", 
                    f"Script not found: {script_path}"
                )
                return
                
            # Determine how to run the script based on extension
            if script_path.endswith('.py'):
                subprocess.Popen(['python3', script_path])
            elif script_path.endswith('.sh'):
                subprocess.Popen(['bash', script_path])
            else:
                # For other scripts, try to execute directly
                subprocess.Popen([script_path])
                
        except Exception as e:
            QMessageBox.warning(
                None, 
                "Error", 
                f"Failed to run script: {e}"
            )
    
    def run(self):
        """Run the application main loop"""
        # Store the original refresh_items method
        original_refresh_items = self.manager_window.refresh_items
        
        # Update menu when data changes
        self.manager_window.refresh_items = lambda: (
            original_refresh_items(),
            self.update_tray_menu()
        )
        
        # Start the application event loop
        return self.app.exec_()