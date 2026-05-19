"""
Firebase Storage Service for Audio File Management
Handles uploading and managing audio files in Firebase Storage
"""
import logging
from typing import Dict, Optional
import uuid
from datetime import datetime
from app.config_firebase import get_storage_bucket

logger = logging.getLogger(__name__)


class FirebaseStorageService:
    """Service for managing audio files in Firebase Storage"""
    
    def __init__(self):
        """Initialize Firebase Storage Service"""
        self.bucket = get_storage_bucket()
        self.base_path = "audios"
    
    def upload_audio(
        self, 
        audio_bytes: bytes, 
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Dict:
        """
        Upload audio file to Firebase Storage
        
        Args:
            audio_bytes: Raw audio data (bytes)
            user_id: Optional user ID for organization
            session_id: Optional session ID for tracking
            
        Returns:
            Dictionary with:
            - status: "success" or "error"
            - url: Public URL to the audio file
            - path: Storage path in Firebase
            - size_bytes: File size
            - error: Error message if failed
        """
        try:
            # Generate unique filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            unique_id = uuid.uuid4().hex[:8]
            filename = f"audio_{timestamp}_{unique_id}.mp3"
            
            # Organize in folders by date and user/session
            if user_id:
                path = f"{self.base_path}/users/{user_id}/{datetime.utcnow().strftime('%Y/%m/%d')}/{filename}"
            elif session_id:
                path = f"{self.base_path}/sessions/{session_id}/{datetime.utcnow().strftime('%Y/%m/%d')}/{filename}"
            else:
                path = f"{self.base_path}/anonymous/{datetime.utcnow().strftime('%Y/%m/%d')}/{filename}"
            
            # Create blob reference
            blob = self.bucket.blob(path)
            
            # Upload file with metadata
            blob.upload_from_string(
                audio_bytes,
                content_type='audio/mpeg',
                timeout=30
            )
            
            # Set metadata for tracking
            metadata = {
                'originalFilename': filename,
                'uploadedAt': datetime.utcnow().isoformat(),
                'userId': user_id or 'anonymous',
                'sessionId': session_id or 'unknown'
            }
            blob.metadata = metadata
            blob.patch()
            
            # Make file publicly readable
            blob.make_public()
            
            # Get public URL
            public_url = blob.public_url
            
            logger.info(
                f"✅ Audio uploaded to Firebase | "
                f"Path: {path} | "
                f"Size: {len(audio_bytes)} bytes | "
                f"URL: {public_url}"
            )
            
            return {
                "status": "success",
                "url": public_url,
                "path": path,
                "size_bytes": len(audio_bytes),
                "filename": filename
            }
        
        except Exception as e:
            logger.error(f"❌ Firebase upload failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "url": None,
                "path": None,
                "size_bytes": 0,
                "filename": None
            }
    
    def delete_audio(self, storage_path: str) -> Dict:
        """
        Delete an audio file from Firebase Storage
        
        Args:
            storage_path: Path to the file in Firebase Storage
            
        Returns:
            Dictionary with status and message
        """
        try:
            blob = self.bucket.blob(storage_path)
            blob.delete()
            
            logger.info(f"✅ Audio deleted from Firebase | Path: {storage_path}")
            
            return {
                "status": "success",
                "message": f"File deleted: {storage_path}"
            }
        
        except Exception as e:
            logger.error(f"❌ Firebase delete failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def get_file_url(self, storage_path: str) -> str:
        """
        Get public URL for a file
        
        Args:
            storage_path: Path to the file in Firebase Storage
            
        Returns:
            Public URL to the file
        """
        try:
            blob = self.bucket.blob(storage_path)
            blob.make_public()
            return blob.public_url
        except Exception as e:
            logger.error(f"❌ Failed to get URL: {str(e)}")
            return ""


# Global instance
firebase_storage = FirebaseStorageService()
