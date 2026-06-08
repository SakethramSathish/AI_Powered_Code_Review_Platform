import logging
import os
from config.settings import settings

# Ensure the logs directory exists
os.makedirs(settings.LOGS_DIR, exist_ok=True)

# Configure the global logging format
logging.basicConfig(
    filename=os.path.join(settings.LOGS_DIR, "game_engine.log"),
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def get_logger(module_name: str) -> logging.Logger:
    """
    Returns a configured logger instance for a specific module.
    Usage: logger = get_logger(__name__)
    """
    return logging.getLogger(module_name)