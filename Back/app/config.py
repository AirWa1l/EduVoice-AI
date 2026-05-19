"""
Configuration module for EduVoice backend
Loads environment variables and stores application settings
"""
import os
import json
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables"""
    
    # =====================================
    # Google Gemini API Configuration
    # =====================================
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # =====================================
    # Eleven Labs TTS Configuration
    # =====================================
    ELEVEN_LABS_API_KEY: str = os.getenv("ELEVEN_LABS_API_KEY", "")
    ELEVEN_LABS_VOICE_ID: str = os.getenv("ELEVEN_LABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
    ELEVEN_LABS_API_URL: str = "https://api.elevenlabs.io/v1/text-to-speech"
    
    # =====================================
    # Firebase Configuration
    # =====================================
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID", "")
    FIREBASE_STORAGE_BUCKET: str = os.getenv("FIREBASE_STORAGE_BUCKET", "")
    
    # Firebase credentials handling for production
    # Prefer JSON string from env var (for Docker/Cloud environments)
    # Fall back to file path (for local development)
    @staticmethod
    def get_firebase_credentials() -> dict:
        """
        Get Firebase credentials from environment
        Priority: FIREBASE_CREDENTIALS_JSON > FIREBASE_CREDENTIALS_PATH
        """
        # Try to get credentials from JSON string (production)
        credentials_json = os.getenv("FIREBASE_CREDENTIALS_JSON", "")
        if credentials_json:
            try:
                return json.loads(credentials_json)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON in FIREBASE_CREDENTIALS_JSON environment variable")
        
        # Fall back to file path (local development only)
        credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH", ".firebase-credentials.json")
        if os.path.exists(credentials_path):
            try:
                with open(credentials_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                raise ValueError(f"Failed to load Firebase credentials from {credentials_path}: {str(e)}")
        
        raise ValueError("Firebase credentials not found. Set FIREBASE_CREDENTIALS_JSON or FIREBASE_CREDENTIALS_PATH")
    
    # =====================================
    # Google OAuth Configuration
    # =====================================
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    
    # =====================================
    # Application Settings
    # =====================================
    APP_NAME: str = os.getenv("APP_NAME", "EduVoice API")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # CORS Origins
    CORS_ORIGINS: list = [
        origin.strip() 
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
    ]
    
    # =====================================
    # Request Settings
    # =====================================
    MAX_TEXT_LENGTH: int = 500
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    
    # =====================================
    # Validation
    # =====================================
    def validate(self):
        """Validate that all required settings are configured"""
        missing = []
        
        # Required API keys
        if not self.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY")
        if not self.ELEVEN_LABS_API_KEY:
            missing.append("ELEVEN_LABS_API_KEY")
        if not self.FIREBASE_PROJECT_ID:
            missing.append("FIREBASE_PROJECT_ID")
        if not self.FIREBASE_STORAGE_BUCKET:
            missing.append("FIREBASE_STORAGE_BUCKET")
        
        # Try to load Firebase credentials
        try:
            self.get_firebase_credentials()
        except ValueError as e:
            missing.append(f"Firebase credentials: {str(e)}")
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")


settings = Settings()
