"""
Configuration module for EduVoice backend
Loads environment variables and stores application settings
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables"""
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    ELEVEN_LABS_API_KEY: str = os.getenv("ELEVEN_LABS_API_KEY", "")
    ELEVEN_LABS_VOICE_ID: str = os.getenv("ELEVEN_LABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
    
    # API Endpoints
    GEMINI_API_URL: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    ELEVEN_LABS_API_URL: str = "https://api.elevenlabs.io/v1/text-to-speech"
    
    # App Settings
    APP_NAME: str = "EduVoice API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Request Settings
    MAX_TEXT_LENGTH: int = 500
    REQUEST_TIMEOUT: int = 30
    
    # Validation
    def validate(self):
        """Validate that all required settings are configured"""
        if not self.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        if not self.ELEVEN_LABS_API_KEY:
            raise ValueError("ELEVEN_LABS_API_KEY environment variable is not set")


settings = Settings()
