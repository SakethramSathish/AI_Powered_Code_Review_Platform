from models.player import Player

class AdaptiveEngine:
    """
    Analyzes player behaviour and state to dynamically adjust game tone,
    NPC reactions, and determine the story's overall trajectory.
    """

    @staticmethod
    def evaluate_trajectory(player: Player) -> str:
        """
        Evaluates the player's current alignment to determine which ending path they are on.
        """
        if player.alignment_score >= 20:
            return "Heroic Path"
        elif player.alignment_score <= -20:
            return "Villainous Path"
        else:
            return "Neutral Path"
        
    @staticmethod
    def get_tone_modifier(player: Player) -> str:
        """
        Provides a tone modifier to inject into the LLm prompt based on how the player is acting.
        """
        if player.alignment == "heroic":
            return "The world reacts with hope and admiration. NPCs are generally trusting."
        elif player.alignment == "villainous":
            return "The world reacts with fear, hostility, and darkness. NPCs are wary or aggressive."
        else:
            return "The world reacts indifferently, waiting to see the player's true colors."