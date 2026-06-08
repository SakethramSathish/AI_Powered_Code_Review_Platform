import json
import os
from config.settings import settings

class SaveLoadManager:
    """Handles serializing and deserializing the game state to JSON."""

    @staticmethod
    def save_game(state_dict: dict, filename: str = "autosave.json") -> bool:
        """Saves the current game state dictionary to a JSON file."""
        filepath = os.path.join(settings.SAVES_DIR, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                # indent=4 makes the JSON human-readable for debugging
                json.dump(state_dict, f, indent=4)
            return True
        except Exception as e:
            # In a production environment, use a proper logger here
            print(f"Failed to save game: {e}")
            return False

    @staticmethod
    def load_game(filename: str = "autosave.json") -> dict:
        """Loads a game state dictionary from a JSON file."""
        filepath = os.path.join(settings.SAVES_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f"Save file not found: {filepath}")
            return None
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Corrupted save file: {e}")
            return None
        except Exception as e:
            print(f"Failed to load game: {e}")
            return None
            
    @staticmethod
    def list_saves() -> list:
        """Returns a list of all available save file names in the directory."""
        try:
            saves = [f for f in os.listdir(settings.SAVES_DIR) if f.endswith('.json')]
            # Sort chronologically or alphabetically if desired
            return sorted(saves)
        except Exception as e:
            print(f"Could not list saves: {e}")
            return []