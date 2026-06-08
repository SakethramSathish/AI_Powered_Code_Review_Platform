import os
import sys
import streamlit as st

# Ensure project root is in sys.path so 'core', 'config', etc. can be imported.
# Also remove the script directory from sys.path to prevent 'app.py' from shadowing the 'app' package.
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)
if script_dir in sys.path:
    sys.path.remove(script_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

#Import the core engine
from core.engine import GameEngine

#Import UI modules
from app.ui.theme import apply_theme
from app.ui.sidebar import render_sidebar
from app.ui.components import render_story_screen, render_choices
from config.constants import GameConstants
from utils.validators import InputValidator

#1. Apply the visual theme and page config first
apply_theme()

# 2. Initialize the Game Engine in Streamlit's session state
# This ensures the engine and memory persist across button clicks
if 'engine' not in st.session_state:
    st.session_state.engine = GameEngine(player_name=GameConstants.DEFAULT_PLAYER_NAME)

def main():
    engine = st.session_state.engine

    #3. Render the sidebar
    render_sidebar(engine)

    #Main UI header
    st.title(GameConstants.UI_TITLE)
    st.markdown(f"*{GameConstants.UI_SUBTITLE}*")
    st.divider()

    ui_state = engine.get_ui_state()

    #4. GAME INITIALIZATION STATE
    #If the default scene text is still present, the game hasn't started.
    if ui_state["chapter"] == 1 and ui_state["scene_text"] == "The story has not yet begun.":
        st.write("### Welcome to your adventure.")
        
        # Setup player name
        raw_name = st.text_input("Enter your character's name:", value="Wanderer")
        
        # Setup genre, including the custom free-text option we discussed
        genres = GameConstants.AVAILABLE_GENRES + ["🎲 Custom Genre..."]
        genre_choice = st.selectbox("Choose your starting realm:", genres)
        
        if genre_choice == "🎲 Custom Genre...":
            raw_genre = st.text_input("Type your custom genre:", placeholder="e.g., Underwater Steampunk")
        else:
            raw_genre = genre_choice
            
        if st.button("Begin Story", use_container_width=True):
            # Sanitize inputs before passing to the backend
            final_name = InputValidator.sanitize_player_name(raw_name)
            final_genre = InputValidator.sanitize_custom_genre(raw_genre)
            
            # Update name in state and start game
            engine.state_manager.player.name = final_name
            with st.spinner("The AI is weaving your world..."):
                engine.start_new_game(final_genre)
            st.rerun() # Refresh the page to show the first scene
            
        return # Stop rendering the rest of the page until they click start

    # 5. MAIN GAME LOOP STATE
    # Render the story text and history
    render_story_screen(ui_state)

    # If the game is not over, render the choices
    if not ui_state.get("game_over", False):
        selected_choice = render_choices(ui_state["choices"])
        
        # If the player clicked a button, process the turn
        if selected_choice:
            with st.spinner("The AI is calculating the consequences of your actions..."):
                engine.take_turn(selected_choice)
            st.rerun() # Refresh the UI with the new AI response

if __name__ == "__main__":
    main()