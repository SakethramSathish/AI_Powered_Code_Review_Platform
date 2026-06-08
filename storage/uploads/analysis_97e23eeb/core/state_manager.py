from models.player import Player
from models.story import StoryState
from models.memory import Memory
from core.memory_manager import MemoryManager

class StateManager:
    """
    Holds all game data models and coordinates updates between them.
    """

    def __init__(self, player_name: str = "Wanderer"):
        #Initialize core data models
        self.player = Player(name=player_name)
        self.story = StoryState()
        self.memory = Memory()

        #Initialize the memory controller
        self.memory_manager = MemoryManager(self.memory)
    
    def update_from_llm_response(self, player_choice: str, llm_response: dict):
        """
        Takes the parsed JSON from the AI and updates all relevant game states.
        """
        # 1. Log the player's choice in memory
        if player_choice:
            self.memory_manager.log_choice(player_choice)
            
        # 2. Extract data from LLM response safely
        new_scene = llm_response.get("scene_text", "The world fades to white...")
        new_choices = llm_response.get("choices", ["Continue"])
        alignment_shift = llm_response.get("alignment_shift", 0)
        
        # 3. Update Player Alignment based on their action
        if alignment_shift != 0:
            self.player.update_alignment(alignment_shift)
            
        # 4. Update Story State
        # Save the old scene to history before overwriting it
        self.story.add_to_history(self.story.current_scene)
        
        # Set the new scene and the new choices
        self.story.update_scene(new_scene, new_choices)
        self.story.advance_chapter()
        
        # 5. Automatically log the new scene as a key event for the LLM's context
        # We grab just the first 60 characters so we don't bloat the token count
        event_summary = f"Chapter {self.story.chapter}: {new_scene[:60]}..."
        self.memory_manager.log_event(event_summary)

    def get_state_dict(self) -> dict:
        """
        Packages the entire game state into a single dict for saving.
        """
        return{
            "player": self.player.to_dict(),
            "story": self.story.to_dict(),
            "memory": self.memory.to_dict()
        }
    
    def load_from_dict(self, data: dict):
        """
        Restores the game from a loaded dictionary.
        """
        self.player = Player.from_dict(data.get("player", {}))
        self.story = StoryState.from_dict(data.get("story", {}))
        self.memory = Memory.from_dict(data.get("memory", {}))

        #Re-initialize the manager with the loaded memory
        self.memory_manager = MemoryManager(self.memory)