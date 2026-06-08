class InputValidator:
    """Sanitizes and validates user input before it reaches the game engine."""

    @staticmethod
    def sanitize_custom_genre(genre_input: str, fallback: str = "High Fantasy") -> str:
        """
        Ensures a custom genre input is safe, not empty, and within character limits 
        to prevent prompt injection or token bloating.
        """
        if not genre_input or not isinstance(genre_input, str):
            return fallback
            
        cleaned_input = genre_input.strip()
        
        if not cleaned_input:
            return fallback
            
        # Limit the genre description to 50 characters
        return cleaned_input[:50]

    @staticmethod
    def sanitize_player_name(name_input: str, fallback: str = "Wanderer") -> str:
        """Validates the player's custom name."""
        if not name_input or not isinstance(name_input, str):
            return fallback
            
        cleaned_name = name_input.strip()
        
        if not cleaned_name:
            return fallback
            
        # Limit names to 20 characters and remove line breaks
        cleaned_name = cleaned_name.replace('\n', '').replace('\r', '')
        return cleaned_name[:20]