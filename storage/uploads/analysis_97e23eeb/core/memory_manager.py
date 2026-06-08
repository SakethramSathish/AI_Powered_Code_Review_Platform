from models.memory import Memory
from config.settings import settings

class MemoryManager:
    """
    Controller for the game's memory.
    Ensures the data stays relevant and within the LLM's token limits.
    """

    def __init__(self, memory_model: Memory):
        #We pass the raw data model into this manager.
        self.memory = memory_model

    def log_choice(self, choice: str):
        """Logs a player's choice and enforces the history limit."""
        self.memory.record_choice(choice)

        #If we exceed the max history, remove the oldest item (FIFO)
        if len(self.memory.past_choices) > settings.MAX_MEMORY_HISTORY:
            self.memory.past_choices.pop(0)

    def log_event(self, event: str):
        """Logs a significant event and enforces the history limit."""
        self.memory.record_event(event)
        
        # If we exceed the max history, remove the oldest item (FIFO)
        if len(self.memory.key_events) > settings.MAX_MEMORY_HISTORY:
            self.memory.key_events.pop(0)

    def adjust_relationship(self, character_name: str, score_change: int):
        """Updates how an NPC feels about the player."""
        if score_change != 0:
            self.memory.update_relationship(character_name, score_change)

    def get_llm_context(self) -> str:
        """Fetches the formatted, token-safe context string for the LLM."""
        return self.memory.get_context_summary(max_items=settings.MAX_MEMORY_HISTORY)
    
    