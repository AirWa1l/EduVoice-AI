"""
Firebase Configuration and Initialization
Handles Firebase Admin SDK setup for production and development
"""
import logging
import firebase_admin
from firebase_admin import credentials, storage
from app.config import settings

logger = logging.getLogger(__name__)

# Global Firebase app instance
_firebase_app = None
_storage_bucket = None


def init_firebase():
    """
    Initialize Firebase Admin SDK
    Loads credentials from environment variables or file
    
    Raises:
        ValueError: If Firebase credentials are not properly configured
    """
    global _firebase_app, _storage_bucket
    
    try:
        # Get credentials from config
        creds_dict = settings.get_firebase_credentials()
        
        # Initialize Firebase only once
        if not firebase_admin._apps:
            cred = credentials.Certificate(creds_dict)
            _firebase_app = firebase_admin.initialize_app(
                cred,
                {
                    'storageBucket': settings.FIREBASE_STORAGE_BUCKET
                }
            )
            logger.info(f"Firebase initialized successfully for project: {settings.FIREBASE_PROJECT_ID}")
        else:
            _firebase_app = firebase_admin.get_app()
        
        # Get storage bucket reference
        _storage_bucket = storage.bucket()
        logger.info(f"Firebase Storage bucket ready: {_storage_bucket.name}")
        
    except Exception as e:
        logger.error(f"Firebase initialization failed: {str(e)}")
        raise


def get_storage_bucket():
    """
    Get Firebase Storage bucket instance
    Initializes Firebase if not already done
    
    Returns:
        google.cloud.storage.Bucket: Firebase Storage bucket
    """
    global _storage_bucket
    
    if _storage_bucket is None:
        init_firebase()
    
    return _storage_bucket


def is_firebase_ready() -> bool:
    """
    Check if Firebase is properly initialized
    
    Returns:
        bool: True if Firebase is ready, False otherwise
    """
    try:
        bucket = get_storage_bucket()
        return bucket is not None
    except Exception as e:
        logger.error(f"Firebase health check failed: {str(e)}")
        return False


# Initialize Firebase on module load
try:
    init_firebase()
except Exception as e:
    logger.warning(f"Firebase will be initialized on first use: {str(e)}")
