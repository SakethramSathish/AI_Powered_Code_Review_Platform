import streamlit as st

def render_story_screen(ui_state: dict):
    """Renders the main narrative text and the player's history."""
    
    # 1. Display the "Story So Far" in a collapsible expander
    # This keeps the screen clean but lets the player review past events
    history = ui_state.get("history", [])
    if history:
        with st.expander("📖 The Story So Far...", expanded=False):
            for past_scene in history:
                # Using the custom CSS class we defined in theme.py
                st.markdown(f"<div class='choice-history'>{past_scene}</div>", unsafe_allow_html=True)
                st.markdown("---")
    
    # 2. Display the current scene
    # We check if the game is over to apply the special 'epilogue-text' styling
    if ui_state.get("game_over", False):
        st.markdown(f"<div class='epilogue-text'>{ui_state['scene_text']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='story-text'>{ui_state['scene_text']}</div>", unsafe_allow_html=True)

def render_choices(choices: list) -> str:
    """
    Renders the action buttons for the player.
    Returns the string of the selected choice, or None if nothing is clicked.
    """
    st.write("### What do you do next?")
    
    if not choices:
        return None

    selected_choice = None
    
    # We render the buttons vertically because AI-generated choices 
    # can sometimes be long sentences, which breaks horizontal columns.
    for i, choice in enumerate(choices):
        # use_container_width makes the buttons stretch nicely across the screen
        if st.button(choice, key=f"btn_{i}", use_container_width=True):
            selected_choice = choice
            
    return selected_choice