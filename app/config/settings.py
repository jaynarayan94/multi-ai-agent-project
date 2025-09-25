from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    groq_api_key: str = os.getenv("GROQ_API_KEY")
    tavila_api_key: str = os.getenv("TAVILA_API_KEY")

    ALLOWED_MODEL_NAMES = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant"
        ]

settings = Settings()

if not settings.groq_api_key or not settings.tavila_api_key:
    raise ValueError("API keys for GROQ and TAVILA must be set in the environment variables.")
