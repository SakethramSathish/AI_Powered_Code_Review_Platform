import streamlit as st
from config.constants import GameConstants

def apply_theme():
    """Applies the page configuration and custom CSS for the game."""
    
    # 1. Set the page configuration (Must be the first Streamlit command)
    st.set_page_config(
        page_title=GameConstants.UI_TITLE,
        page_icon="🧠",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    # 2. Inject Custom CSS to make it feel more like a game
    st.markdown("""
        <style>
        /* Main story text styling */
        .story-text {
            font-size: 1.2rem;
            line-height: 1.8;
            font-family: 'Georgia', serif;
            padding: 20px;
            background-color: rgba(30, 30, 30, 0.5);
            border-radius: 10px;
            border-left: 4px solid #6366f1;
            margin-bottom: 20px;
        }
        
        /* Highlight previous choices */
        .choice-history {
            color: #a1a1aa;
            font-style: italic;
            font-size: 0.9rem;
        }

        /* Ending text styling */
        .epilogue-text {
            font-size: 1.3rem;
            font-weight: bold;
            color: #fbbf24;
            text-align: center;
            padding: 30px;
            background-color: rgba(0, 0, 0, 0.3);
            border: 1px solid #fbbf24;
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)