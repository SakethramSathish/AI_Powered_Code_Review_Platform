from core.state_manager import StateManager
from ai.story_generator import story_generator
from core.adaptive_engine import AdaptiveEngine
from core.ending_engine import EndingEngine

class GameEngine:
    """
    The main game loop controller. 
    Now fully integrated with adaptive tone modifiers and the ending generator.
    """
    def __init__(self, player_name: str = "Wanderer", max_chapters: int = 5):
        self.state_manager = StateManager(player_name=player_name)
        self.max_chapters = max_chapters
        self.game_over = False
        
    def start_new_game(self, genre: str):
        """Initializes the game and generates the very first scene."""
        self.game_over = False
        initial_setup = f"The player has just begun a new {genre} adventure. Introduce the setting and present the first set of choices."
        
        response = story_generator.generate_next_beat(
            player=self.state_manager.player,
            memory=self.state_manager.memory,
            previous_scene=initial_setup,
            player_choice="Begin the adventure."
        )
        
        self.state_manager.update_from_llm_response("Begin the adventure.", response)

    def take_turn(self, player_choice: str):
        """Processes a player's choice and advances the story."""
        if self.game_over:
            return

        # 1. Fetch current scene
        current_scene = self.state_manager.story.current_scene
        
        # 2. ADAPTIVE ENGINE: Get the tone modifier based on the player's alignment
        tone_modifier = AdaptiveEngine.get_tone_modifier(self.state_manager.player)
        
        # Inject the tone directly into the context so the AI subtly shifts its writing style
        scene_with_tone = f"{current_scene}\n\n[System Directive for Tone: {tone_modifier}]"
        
        # 3. Generate the next beat
        response = story_generator.generate_next_beat(
            player=self.state_manager.player,
            memory=self.state_manager.memory,
            previous_scene=scene_with_tone,
            player_choice=player_choice
        )
        
        # 4. Update state
        self.state_manager.update_from_llm_response(player_choice, response)

        # 5. ENDING ENGINE: Check if we've reached the final chapter
        if self.state_manager.story.chapter >= self.max_chapters:
            self._trigger_ending()

    def _trigger_ending(self):
        """Handles the game over sequence using the Ending Engine."""
        self.game_over = True
        
        # Ask the Ending Engine to write the final epilogue
        epilogue = EndingEngine.generate_epilogue(
            player=self.state_manager.player,
            memory=self.state_manager.memory
        )
        
        # Force the UI to display the epilogue and remove playable choices
        self.state_manager.story.update_scene(
            new_scene=f"### 🏁 EPILOGUE: {AdaptiveEngine.evaluate_trajectory(self.state_manager.player)}\n\n{epilogue}", 
            new_choices=["Restart Game"]
        )

    def get_ui_state(self) -> dict:
        """Returns only the necessary data for the frontend to render the game."""
        return {
            "chapter": self.state_manager.story.chapter,
            "max_chapters": self.max_chapters,
            "scene_text": self.state_manager.story.current_scene,
            "choices": self.state_manager.story.available_choices,
            "player_name": self.state_manager.player.name,
            "alignment": self.state_manager.player.alignment,
            "alignment_score": self.state_manager.player.alignment_score,
            "history": self.state_manager.story.story_history,
            "game_over": self.game_over
        }

    def get_full_save_state(self) -> dict:
        """Exposes the full state dictionary for saving the game."""
        # Get the core data models
        save_data = self.state_manager.get_state_dict()
        
        # Inject the engine's specific state into the dictionary
        save_data["engine_state"] = {
            "max_chapters": self.max_chapters,
            "game_over": self.game_over
        }
        return save_data

    def load_save_state(self, save_data: dict):
        """Restores the engine's state from a loaded save file."""
        # Restore core data models
        self.state_manager.load_from_dict(save_data)
        
        # Restore engine-specific state
        engine_state = save_data.get("engine_state", {})
        self.max_chapters = engine_state.get("max_chapters", 5)
        self.game_over = engine_state.get("game_over", False)