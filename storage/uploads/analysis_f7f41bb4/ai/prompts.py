import json

class PromptTemplates:
    """Stores the prompt templates used to guide the LLM's responses."""

    @staticmethod
    def generate_scene_prompt(
        player_name: str, 
        alignment: str, 
        traits: list, 
        memory_context: str, 
        previous_scene: str, 
        player_choice: str
    ) -> str:
        """
        Builds the prompt to generate the next segment of the story.
        Forces the LLM to output pure JSON.
        """
        traits_str = ", ".join(traits) if traits else "None"
        
        return f"""
You are an expert AI Game Master running a dynamic, interactive fiction game.
Your goal is to generate the next scene based on the player's choice and history.

PLAYER PROFILE:
- Name: {player_name}
- Alignment: {alignment} (This should subtly influence how NPCs react to them)
- Traits: {traits_str}

STORY CONTEXT:
- Memory/History: {memory_context}
- Previous Scene: {previous_scene}
- The Player Chose To: {player_choice}

INSTRUCTIONS:
1. Write the next scene (2-3 paragraphs). Make it immersive, atmospheric, and directly reactive to the player's choice.
2. Provide exactly 3 new choices for the player.
3. Determine if the player's action shifted their alignment (e.g., a cruel act = negative score, a kind act = positive score). Provide an integer from -5 to +5.
4. IMPORTANT: You must respond ONLY with a valid JSON object matching the exact structure below. Do not include markdown formatting like ```json or any conversational text.

EXPECTED JSON FORMAT:
{{
    "scene_text": "The narrative text of what happens next...",
    "choices": [
        "First choice action...",
        "Second choice action...",
        "Third choice action..."
    ],
    "alignment_shift": 2
}}
"""