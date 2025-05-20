import json
import os
from typing import Dict, List, Tuple, Optional

class DataManager:
    """
    Manages the storage and retrieval of script items.
    Each item is a pair of name and script filepath.
    Items are stored in order to maintain their position in menus.
    """
    def __init__(self, data_file: str = "script_items.json"):
        self.data_file = data_file
        self.items = []  # List of (name, script_path) tuples to maintain order
        self._load_data()
    
    def _load_data(self) -> None:
        """Load data from the JSON file if it exists."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    print(f"DEBUG: Loaded data type: {type(data)}, content: {data}")
                    # Handle both old format (dict) and new format (list)
                    if isinstance(data, dict):
                        # Convert old format to new format
                        self.items = [(name, path) for name, path in data.items()]
                        print(f"DEBUG: Converted dict to list: {self.items}")
                    else:
                        self.items = data
                        print(f"DEBUG: Using list directly: {self.items}")
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading data: {e}")
                self.items = []
    
    def _save_data(self) -> None:
        """Save data to the JSON file."""
        try:
            print(f"DEBUG: Saving data: {self.items}")
            with open(self.data_file, 'w') as f:
                json.dump(self.items, f, indent=2)
            print(f"DEBUG: Data saved successfully")
        except IOError as e:
            print(f"Error saving data: {e}")
    
    def add_item(self, name: str, script_path: str) -> bool:
        """
        Add a new script item.
        
        Args:
            name: The display name for the script
            script_path: The filepath to the script
            
        Returns:
            bool: True if added successfully, False otherwise
        """
        if not name or not script_path:
            return False
            
        if not os.path.exists(script_path):
            print(f"Warning: Script path does not exist: {script_path}")
        
        # Check if name already exists
        for i, (item_name, _) in enumerate(self.items):
            if item_name == name:
                # Update existing item
                self.items[i] = (name, script_path)
                self._save_data()
                return True
        
        # Add new item
        self.items.append((name, script_path))
        self._save_data()
        return True
    
    def remove_item(self, name: str) -> bool:
        """
        Remove a script item by name.
        
        Args:
            name: The name of the item to remove
            
        Returns:
            bool: True if removed successfully, False if not found
        """
        for i, (item_name, _) in enumerate(self.items):
            if item_name == name:
                del self.items[i]
                self._save_data()
                return True
        return False
    
    def get_all_items(self) -> List[Tuple[str, str]]:
        """
        Get all script items.
        
        Returns:
            List[Tuple[str, str]]: List of (name, script_path) tuples
        """
        return self.items
    
    def get_item(self, name: str) -> str:
        """
        Get a script path by name.
        
        Args:
            name: The name of the item
            
        Returns:
            str: The script path or empty string if not found
        """
        for item_name, script_path in self.items:
            if item_name == name:
                return script_path
        return ""
    
    def move_item_up(self, name: str) -> bool:
        """
        Move an item up in the list (towards the beginning).
        
        Args:
            name: The name of the item to move
            
        Returns:
            bool: True if moved successfully, False if not found or already at the top
        """
        for i, (item_name, _) in enumerate(self.items):
            if item_name == name:
                if i > 0:  # Not already at the top
                    self.items[i], self.items[i-1] = self.items[i-1], self.items[i]
                    self._save_data()
                    return True
                return False  # Already at the top
        return False  # Item not found
    
    def move_item_down(self, name: str) -> bool:
        """
        Move an item down in the list (towards the end).
        
        Args:
            name: The name of the item to move
            
        Returns:
            bool: True if moved successfully, False if not found or already at the bottom
        """
        for i, (item_name, _) in enumerate(self.items):
            if item_name == name:
                if i < len(self.items) - 1:  # Not already at the bottom
                    self.items[i], self.items[i+1] = self.items[i+1], self.items[i]
                    self._save_data()
                    return True
                return False  # Already at the bottom
        return False  # Item not found
    
    def get_item_index(self, name: str) -> Optional[int]:
        """
        Get the index of an item in the list.
        
        Args:
            name: The name of the item
            
        Returns:
            Optional[int]: The index of the item or None if not found
        """
        for i, (item_name, _) in enumerate(self.items):
            if item_name == name:
                return i
        return None