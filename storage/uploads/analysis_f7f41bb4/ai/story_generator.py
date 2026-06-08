import json
from ai.llm_client import llm_client
from ai.prompts import PromptTemplates
from models.player import Player
from models.memory import Memory

class StoryGenerator:
    """Handles the logic of generating the next story beat using the LLM."""

    def __init__(self):
        self.client = llm_client

    def _clean_json_response(self, text: str) -> dict:
        """
        Cleans the LLM response. Robustly extracts and parses JSON even if
        the LLM includes thinking steps, conversational text, or markdown code blocks.
        """
        text = text.strip()
        
        # Try direct parsing first
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # If that fails, strip markdown code blocks
        clean_text = text
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        elif clean_text.startswith("```"):
            clean_text = clean_text[3:]

        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]

        clean_text = clean_text.strip()
        try:
            return json.loads(clean_text)
        except json.JSONDecodeError:
            pass

        # If it still fails, extract valid {...} block by searching for any '{' and trying to parse.
        # We scan from right to left (last '{' first) to skip any structural placeholders in the thinking prefix.
        import re
        brace_indices = [m.start() for m in re.finditer(r'\{', text)]
        for start_idx in reversed(brace_indices):
            end_idx = text.rfind('}', start_idx)
            if end_idx != -1 and end_idx > start_idx:
                json_candidate = text[start_idx:end_idx+1]
                try:
                    parsed = json.loads(json_candidate)
                    if isinstance(parsed, dict) and ("scene_text" in parsed or "choices" in parsed):
                        return parsed
                except json.JSONDecodeError:
                    pass

        # Fallback response so the game doesn't completely crash if the LLM hallucinates
        print(f"Failed to parse JSON from LLM. Raw output: {text}")
        return {
            "scene_text": "**System Disturbance:** The fabric of reality blurs. The AI narrator lost its train of thought. Please choose an action to stabilize the timeline.",
            "choices": ["Focus my mind", "Look around carefully", "Wait for the world to settle"],
            "alignment_shift": 0
        }
        
    def generate_next_beat(
            self,
            player: Player,
            memory: Memory,
            previous_scene: str,
            player_choice: str
    ) -> dict:
        """Generates the next scene and choices based on current game state."""

        # 1. Build the context string from the memory module
        memory_context = memory.get_context_summary()

        # 2. Construct the strict prompt
        prompt = PromptTemplates.generate_scene_prompt(
            player_name=player.name,
            alignment=player.alignment,
            traits=player.traits,
            memory_context=memory_context,
            previous_scene=previous_scene,
            player_choice=player_choice
        )

        # 3. Call the LLM
        raw_response = self.client.generate_response(prompt)

        # 4. Parse and return the JSON dictionary
        return self._clean_json_response(raw_response)

# Instantiate a global generator
story_generator = StoryGenerator()