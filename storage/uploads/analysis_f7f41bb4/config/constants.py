class GameConstants:
    """Static constants and configuration values for the game."""
    
    # Available story genres for the player to choose from
    AVAILABLE_GENRES = [
        "High Fantasy",
        "Cyberpunk Sci-Fi",
        "Cosmic Horror",
        "Noir Mystery",
        "Post-Apocalyptic"
    ]
    
    # Alignment thresholds for the Adaptive Engine
    ALIGNMENT_HEROIC_THRESHOLD = 20
    ALIGNMENT_VILLAINOUS_THRESHOLD = -20
    
    # Default fallback values
    DEFAULT_PLAYER_NAME = "Wanderer"
    DEFAULT_MAX_CHAPTERS = 5
    
    # UI Strings (Makes it easy to change frontend text in one place)
    UI_TITLE = "🧠 Adaptive AI Story Engine"
    UI_SUBTITLE = "Your choices shape the world."
    UI_ERROR_MSG = "The AI encountered an anomaly. Please try your choice again."