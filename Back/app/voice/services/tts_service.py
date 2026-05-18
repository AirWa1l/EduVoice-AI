"""
TTS Service - Integration with Eleven Labs API
Converts text responses to speech audio
"""
import logging
import requests
import uuid
from typing import Dict, Optional
from app.config import settings
import time
from pathlib import Path

logger = logging.getLogger(__name__)

# Audio storage directory
AUDIO_DIR = Path(__file__).parent.parent.parent / "static" / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


class TTSService:
    """Service for TTS integration with Eleven Labs API"""
    
    def __init__(self, api_key: str = None, voice_id: str = None):
        """
        Initialize TTS Service
        
        Args:
            api_key: Eleven Labs API key
            voice_id: Voice ID to use for TTS
        """
        self.api_key = api_key or settings.ELEVEN_LABS_API_KEY
        self.voice_id = voice_id or settings.ELEVEN_LABS_VOICE_ID
        self.base_url = settings.ELEVEN_LABS_API_URL
        self.timeout = settings.REQUEST_TIMEOUT
        
        self.headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def synthesize(self, text: str, voice_id: Optional[str] = None) -> Dict:
        """
        Synthesize text to speech
        
        Args:
            text: Text to convert to speech
            voice_id: Optional voice ID override
            
        Returns:
            Dictionary with audio data and metadata
        """
        try:
            start_time = time.time()
            
            voice_id = voice_id or self.voice_id
            url = f"{self.base_url}/{voice_id}"
            
            payload = {
                "text": text,
                "model_id": "eleven_flash_v2_5",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }
            
            logger.info(f"Synthesizing text: {text[:50]}... with voice {voice_id}")
            
            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                error_msg = response.json().get("detail", {}).get("message", "Unknown error")
                logger.error(f"TTS API error: {response.status_code} - {error_msg}")
                return {
                    "status": "error",
                    "audio_data": None,
                    "error": f"TTS API error: {error_msg}",
                    "latency_ms": (time.time() - start_time) * 1000
                }
            
            # Save audio to file
            audio_content = response.content
            audio_filename = f"audio_{uuid.uuid4().hex[:8]}.mp3"
            audio_path = AUDIO_DIR / audio_filename
            
            with open(audio_path, 'wb') as f:
                f.write(audio_content)
            
            audio_url = f"/audio/{audio_filename}"
            
            processing_time = (time.time() - start_time) * 1000  # ms
            
            logger.info(f"Audio synthesized successfully in {processing_time:.2f}ms - Saved to {audio_url}")
            
            return {
                "status": "success",
                "audio_data": audio_url,
                "audio_bytes": len(audio_content),
                "latency_ms": processing_time,
                "voice_id": voice_id
            }
        
        except requests.exceptions.RequestException as e:
            logger.error(f"TTS request error: {str(e)}")
            return {
                "status": "error",
                "audio_data": None,
                "error": f"TTS request failed: {str(e)}",
                "latency_ms": (time.time() - start_time) * 1000
            }
        except Exception as e:
            logger.error(f"TTS processing error: {str(e)}")
            return {
                "status": "error",
                "audio_data": None,
                "error": f"TTS processing failed: {str(e)}",
                "latency_ms": (time.time() - start_time) * 1000
            }
    
    def validate_api(self) -> bool:
        """
        Validate that TTS API connection works
        
        Returns:
            True if API is reachable, False otherwise
        """
        try:
            result = self.synthesize("Prueba")
            return result.get("status") == "success"
        except Exception as e:
            logger.error(f"TTS API validation failed: {str(e)}")
            return False


# Global instance
tts_service = TTSService()
