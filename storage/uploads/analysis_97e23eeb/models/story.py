from dataclasses import dataclass, field
from typing import List

@dataclass
class StoryState:
    """Represents the current state and progression of the narrative."""
    current_scene: str = "The story has not yet begun."
    chapter: int = 1
    available_choices: List[str] = field(default_factory=list)
    story_history: List[str] = field(default_factory=list)

    def advance_chapter(self):
        """Increments the chapter counter."""
        self.chapter += 1

    def add_to_history(self, text: str):
        """Appends a completed scene to the overall story history."""
        if text:
            self.story_history.append(text)

    def update_scene(self, new_scene: str, new_choices: List[str]):
        """Updates the current scene and the choices available to the player."""
        self.current_scene = new_scene
        self.available_choices = new_choices

    def to_dict(self) -> dict:
        """Converts the story state to a dictionary for saving."""
        return {
            "current_scene": self.current_scene,
            "chapter": self.chapter,
            "available_choices": self.available_choices,
            "story_history": self.story_history
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'StoryState':
        """Creates a StoryState instance from a dictionary (loading)"""
        return cls(
            current_scene=data.get("current_scene", "The story has not yet begun."),
            chapter=data.get("chapter", 1),
            available_choices=data.get("available_choices", []),
            story_history=data.get("story_history", [])
        )