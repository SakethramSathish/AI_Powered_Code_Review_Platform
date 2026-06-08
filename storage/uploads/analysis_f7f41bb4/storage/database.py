import os
from datetime import datetime
# from pymongo import MongoClient

class DatabaseManager:
    """
    Advanced Storage Module (Phase 3/4).
    Handles connecting to a NoSQL database (MongoDB) for scalable state persistence.
    """
    
    def __init__(self):
        # Fetch the URI from environment variables, defaulting to a local instance
        self.db_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        self.client = None
        self.db = None
        self.collection = None
        
        # NOTE: Uncomment the block below to activate the database connection
        """
        try:
            self.client = MongoClient(self.db_uri)
            self.db = self.client["ai_story_engine"]
            self.collection = self.db["saved_games"]
            print("Successfully connected to MongoDB.")
        except Exception as e:
            print(f"Database connection failed: {e}")
        """

    def save_game_to_db(self, save_slot: str, state_dict: dict) -> bool:
        """Saves or updates the game state in the database."""
        if self.collection is None:
            print("Database not initialized. Please configure MongoDB.")
            return False
            
        try:
            # Use 'upsert' to create a new save or overwrite an existing one
            self.collection.update_one(
                {"save_slot": save_slot},
                {"$set": {
                    "state": state_dict,
                    "last_saved": datetime.now()
                }},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"Failed to save to database: {e}")
            return False

    def load_game_from_db(self, save_slot: str) -> dict:
        """Retrieves a specific game state from the database."""
        if self.collection is None:
            return None
            
        try:
            record = self.collection.find_one({"save_slot": save_slot})
            if record:
                return record.get("state")
            return None
        except Exception as e:
            print(f"Failed to load from database: {e}")
            return None
            
    def list_db_saves(self) -> list:
        """Returns a list of all save slots available in the database."""
        if self.collection is None:
            return []
            
        try:
            # Fetch only the 'save_slot' field for all documents
            records = self.collection.find({}, {"save_slot": 1, "_id": 0})
            return [record["save_slot"] for record in records]
        except Exception as e:
            print(f"Failed to list saves: {e}")
            return []

# Instantiate a global instance to be used if the user switches to DB storage
db_manager = DatabaseManager()