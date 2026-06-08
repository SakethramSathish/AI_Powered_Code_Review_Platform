import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
from pathlib import Path

#Load env variables from a .env file
load_dotenv()

class Settings:
    """Central configuration for the Adaptive AI Story Engine."""

    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing. Please set it in your .env file.")

    # Model Settings
    LLM_MODEL = "gemma-4-31b-it" # Fast and cost-effective for text generation
    MAX_OUTPUT_TOKENS = 800
    TEMPERATURE = 0.7 # Balances creativity and coherence

    #Game Constants
    MAX_MEMORY_HISTORY = 10 #Number of past events to send to LLM for context

    #Directory Setup
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    SAVES_DIR = DATA_DIR / "saves"
    LOGS_DIR = DATA_DIR / "logs"

#Ensure data directories exist upon initialization
Settings.SAVES_DIR.mkdir(parents=True, exist_ok=True)
Settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)

#Instantiate a global settings object to be imported across the app
settings = Settings()