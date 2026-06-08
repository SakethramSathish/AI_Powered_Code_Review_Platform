from dataclasses import dataclass, field
from typing import List

@dataclass
class Player:
    """Represents the user's character in the story."""
    name: str
    alignment: str = "neutral"
    alignment_score: int = 0
    traits: List[str] = field(default_factory=list)

    def update_alignment(self, score_change: int):
        """Updates the player's alignment score and categorizes them."""
        self.alignment_score += score_change

        #Clamp the score between -100 and 100
        self.alignment_score = max(-100, min(100, self.alignment_score))

        #Update the categorical alignment
        if self.alignment_score >=20:
            self.alignment = "heroic"
        elif self.alignment_score <= -20:
            self.alignment = "villainous"
        else:
            self.alignment = "neutral"

    def add_trait(self, trait: str):
        """Adds a personality trait or title to the player."""
        if trait not in self.traits:
            self.traits.append(trait)

    def to_dict(self) -> dict:
        """Converts the player object to a dictionary for saving"""
        return{
            "name": self.name,
            "alignment": self.alignment,
            "alignment_score": self.alignment_score,
            "traits": self.traits
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Player':
        """Creates a Player instance from a dictionary (loading)."""
        return cls(
            name=data.get("name", "Wanderer"),
            alignment=data.get("alignment", "neutral"),
            alignment_score=data.get("alignment_score", 0),
            traits=data.get("traits", [])
        )