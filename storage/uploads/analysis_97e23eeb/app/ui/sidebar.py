import streamlit as st
from storage.save_load import SaveLoadManager
from core.engine import GameEngine

def render_sidebar(engine: GameEngine):
    """Renders the sidebar containing player stats and save/load controls."""
    
    with st.sidebar:
        ui_state = engine.get_ui_state()
        
        st.header("👤 Player Profile")
        st.subheader(ui_state["player_name"])
        
        # Display moral alignment
        alignment = ui_state["alignment"].capitalize()
        score = ui_state["alignment_score"]
        st.write(f"**Path:** {alignment} ({score})")
        
        # Visual indicator for alignment (-100 to 100 normalized to 0.0 to 1.0)
        # 0.0 is pure evil, 0.5 is neutral, 1.0 is pure good
        normalized_score = max(0.0, min(1.0, (score + 100) / 200))
        st.progress(normalized_score, text="Morality Indicator")
        
        st.divider()
        
        # Game Progress
        st.header("📖 Story Progress")
        st.write(f"**Current Chapter:** {ui_state['chapter']} / {ui_state['max_chapters']}")
        
        st.divider()
        
        # Save / Load Mechanics
        st.header("💾 System Data")
        
        # Save Button
        save_filename = f"{ui_state['player_name'].lower().replace(' ', '_')}_save.json"
        if st.button("Save Current Game", use_container_width=True):
            save_data = engine.get_full_save_state()
            if SaveLoadManager.save_game(save_data, save_filename):
                st.success(f"Game saved as {save_filename}!")
            else:
                st.error("Error: Could not save game.")
                
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Load System
        st.write("**Load Previous Game:**")
        available_saves = SaveLoadManager.list_saves()
        
        if available_saves:
            selected_save = st.selectbox("Select a save file", available_saves, label_visibility="collapsed")
            if st.button("Load Game", use_container_width=True):
                loaded_data = SaveLoadManager.load_game(selected_save)
                if loaded_data:
                    engine.load_save_state(loaded_data)
                    st.success("Game loaded successfully!")
                    st.rerun() # Forces Streamlit to refresh the UI with the loaded data
                else:
                    st.error("Save file corrupted or missing.")
        else:
            st.info("No save files found.")