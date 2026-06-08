import time
import google.generativeai as genai
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

class LLMClient:
    """
    Handles all communication with the Gemini/Gemma API.
    Includes support for both JSON and plain-text generation modes,
    robust retries with exponential backoff, and automatic fallback to
    Gemini 2.5 Flash if the primary model (e.g. Gemma 4 31B) encounters 500 errors.
    """

    def __init__(self):
        # Configure the Gemini API with the key from our central settings
        genai.configure(api_key=settings.GEMINI_API_KEY)

        # Primary and Fallback Models
        self.model_name = settings.LLM_MODEL
        self.fallback_model_name = "models/gemini-2.5-flash"

        # Initialize GenerativeModel objects without default configs
        # config is supplied dynamically at call time
        self.model = genai.GenerativeModel(model_name=self.model_name)
        self.fallback_model = genai.GenerativeModel(model_name=self.fallback_model_name)

    def generate_response(self, prompt: str, json_mode: bool = True) -> str:
        """
        Sends a compiled prompt to Gemini/Gemma and returns the generated text.
        Retries up to 3 times on transient failures, then falls back to Gemini 2.5 Flash
        if the primary model fails.
        """
        max_retries = 3
        retry_delay = 1.0  # start with 1 second delay

        # Dynamic generation config
        generation_config = {
            "temperature": settings.TEMPERATURE,
            "max_output_tokens": settings.MAX_OUTPUT_TOKENS,
        }
        if json_mode:
            generation_config["response_mime_type"] = "application/json"

        # 1. Attempt using primary model (with retries)
        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"Attempting content generation with primary model '{self.model_name}' (Attempt {attempt}/{max_retries}, json_mode={json_mode})")
                response = self.model.generate_content(prompt, generation_config=generation_config)
                return response.text
            except Exception as e:
                logger.warning(f"Primary model attempt {attempt} failed with error: {e}")
                if attempt < max_retries:
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    logger.error(f"Primary model '{self.model_name}' failed after {max_retries} attempts.")

        # 2. Fallback to Gemini 2.5 Flash if primary model is different
        primary_clean = self.model_name.replace("models/", "")
        fallback_clean = self.fallback_model_name.replace("models/", "")

        if primary_clean != fallback_clean:
            logger.warning(f"Falling back to highly-stable '{self.fallback_model_name}' (json_mode={json_mode}) to prevent game disruption...")
            try:
                response = self.fallback_model.generate_content(prompt, generation_config=generation_config)
                logger.info("Successfully recovered game state using fallback model!")
                return response.text
            except Exception as fallback_err:
                logger.error(f"Fallback model also failed: {fallback_err}")

        # 3. If everything fails, return structured system error
        if json_mode:
            # Return a valid JSON error structure so the game state is updated gracefully rather than crashing
            return """{
                "scene_text": "**System Error:** The AI narrator is currently lost in thought. Please check your API key, internet connection, or try again.",
                "choices": ["Focus my mind", "Look around carefully", "Wait for the world to settle"],
                "alignment_shift": 0
            }"""
        else:
            return "**System Error:** The AI narrator is currently lost in thought. Please check your API key, internet connection, or try again."

# Instantiate a single global client to be imported and used by the story generator
llm_client = LLMClient()