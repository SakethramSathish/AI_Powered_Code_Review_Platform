from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Memory:
    """Tracks player decisions, relationships, and key events for LLM context."""
    past_choices: List[str] = field(default_factory=list)
    key_events: List[str] = field(default_factory=list)
    relationships: Dict[str, int] = field(default_factory=dict)

    def record_choice(self, choice: str):
        """Logs a choice made by the player."""
        self.past_choices.append(choice)

    def record_event(self, event: str):
        """Logs a significant story event."""
        self.key_events.append(event)

    def update_relationship(self, character_name: str, score_change: int):
        """Updates the relationship score with a specific NPC."""
        if character_name not in self.relationships:
            self.relationships[character_name] = 0

        self.relationships[character_name] += score_change

    def get_context_summary(self, max_items: int = 5) -> str:
        """Formats the memory into a concise string to inject into the LLM prompt."""
        context_parts = []

        if self.key_events:
            #Grab only the most recent events to save tokens
            recent_events = self.key_events[-max_items:]
            context_parts.append("Key Events: " + ", ".join(recent_events))

        if self.past_choices:
            recent_choices = self.past_choices[-max_items:]
            context_parts.append("Recent Choices: " + ", ".join(recent_choices))

        if self.relationships:
            rels = [f"{char} ({score})" for char, score in self.relationships.items()]
            context_parts.append(f"Relationships: {', '.join(rels)}")

        if not context_parts:
            return "No significant history yet."
        
        return " | ".join(context_parts)
    
    def to_dict(self) -> dict:
        """Converts memory to a dictionary for saving."""
        return{
            "past_choices": self.past_choices,
            "key_events": self.key_events,
            "relationships": self.relationships
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Memory':
        """Creates a Memory instance from a dictionary (loading)"""
        return cls(
            past_choices = data.get("past_choices", []),
            key_events = data.get("key_events", []),
            relationships = data.get("relationships", {})
        )
    
    