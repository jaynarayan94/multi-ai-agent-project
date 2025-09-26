from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    groq_api_key: str = os.getenv("GROQ_API_KEY")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY")

    ALLOWED_MODEL_NAMES = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant"
        ]

settings = Settings()

if not settings.groq_api_key or not settings.tavily_api_key:
    raise ValueError("API keys for GROQ and TAVILY must be set in the environment variables.")
