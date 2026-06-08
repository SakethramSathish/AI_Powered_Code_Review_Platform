from models.player import Player
from models.memory import Memory
from ai.llm_client import llm_client

class EndingEngine:
    """
    Handles the generation of the final story conclusion when the game ends.
    """
    
    @staticmethod
    def generate_epilogue(player: Player, memory: Memory) -> str:
        """
        Generates a custom epilogue using the LLM based on the player's 
        final alignment and accumulated memory history.
        """
        # Determine the type of ending based on their moral alignment
        if player.alignment_score >= 20:
            ending_directive = "Heroic Ending: The player saved the day, but focus on the lingering consequences."
        elif player.alignment_score <= -20:
            ending_directive = "Villainous Ending: The player conquered or destroyed. Describe the ruin they left behind."
        else:
            ending_directive = "Neutral Ending: The player survived and walked away from the main conflict. A bittersweet departure."

        # Grab a summary of their deeds to inject into the ending
        memory_summary = memory.get_context_summary(max_items=10)

        # Construct a unique prompt just for the ending
        prompt = f"""
You are an expert AI storyteller concluding an epic interactive fiction game.

PLAYER PROFILE:
- Name: {player.name}
- Final Alignment: {player.alignment} (Score: {player.alignment_score})
- Traits: {", ".join(player.traits) if player.traits else "None"}

STORY HISTORY:
{memory_summary}

ENDING DIRECTIVE:
Write a highly dramatic, satisfying 3-paragraph epilogue based on this trajectory: "{ending_directive}"

Focus heavily on referencing their specific past choices from the history provided. Show how the world remembers them.
Do NOT provide choices. Respond ONLY with the rich, narrative text of the epilogue. No markdown or JSON.
"""
        
        # Fetch the final narrative from the LLM directly
        try:
            epilogue = llm_client.generate_response(prompt, json_mode=False)
            return epilogue
        except Exception as e:
            print(f"Error generating ending: {e}")
            return "The story ends here, lost to the sands of time. (System Error generating ending)"