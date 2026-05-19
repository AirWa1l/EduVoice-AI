"""
TTS Service - Integration with Eleven Labs API
Converts text responses to speech audio and stores in Firebase Storage
"""
import logging
import requests
from typing import Dict, Optional
from app.config import settings
from app.voice.services.firebase_storage_service import firebase_storage
import time

logger = logging.getLogger(__name__)


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
    
    def synthesize(self, text: str, voice_id: Optional[str] = None, user_id: Optional[str] = None, session_id: Optional[str] = None) -> Dict:
        """
        Synthesize text to speech and upload to Firebase Storage
        
        Args:
            text: Text to convert to speech
            voice_id: Optional voice ID override
            user_id: Optional user ID for organization in Firebase
            session_id: Optional session ID for tracking
            
        Returns:
            Dictionary with audio URL and metadata
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
            
            logger.info(f"🎙️ Synthesizing text: {text[:50]}... with voice {voice_id}")
            
            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                error_msg = response.json().get("detail", {}).get("message", "Unknown error")
                logger.error(f"❌ TTS API error: {response.status_code} - {error_msg}")
                return {
                    "status": "error",
                    "audio_data": None,
                    "error": f"TTS API error: {error_msg}",
                    "latency_ms": (time.time() - start_time) * 1000
                }
            
            # Get audio content
            audio_content = response.content
            
            # Upload to Firebase Storage
            logger.info(f"📤 Uploading audio to Firebase Storage...")
            upload_result = firebase_storage.upload_audio(
                audio_content,
                user_id=user_id,
                session_id=session_id
            )
            
            if upload_result["status"] != "success":
                logger.error(f"❌ Firebase upload failed: {upload_result.get('error')}")
                return {
                    "status": "error",
                    "audio_data": None,
                    "error": f"Firebase upload failed: {upload_result.get('error')}",
                    "latency_ms": (time.time() - start_time) * 1000
                }
            
            processing_time = (time.time() - start_time) * 1000  # ms
            audio_url = upload_result["url"]
            
            logger.info(f"✅ Audio synthesized and stored in {processing_time:.2f}ms | URL: {audio_url}")
            
            return {
                "status": "success",
                "audio_data": audio_url,
                "audio_bytes": len(audio_content),
                "latency_ms": processing_time,
                "voice_id": voice_id,
                "storage_path": upload_result.get("path")
            }
        
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ TTS request error: {str(e)}")
            return {
                "status": "error",
                "audio_data": None,
                "error": f"TTS request failed: {str(e)}",
                "latency_ms": (time.time() - start_time) * 1000
            }
        except Exception as e:
            logger.error(f"❌ TTS processing error: {str(e)}")
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
