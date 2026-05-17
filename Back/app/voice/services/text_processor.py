"""
Text processing service
Handles text validation, cleaning, and preprocessing
"""
import re
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


class TextProcessor:
    """Handles text cleaning and validation for voice input"""
    
    def __init__(self, max_length: int = 500):
        self.max_length = max_length
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize input text
        
        Args:
            text: Raw text from STT
            
        Returns:
            Cleaned text
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep punctuation for sentences
        text = re.sub(r'[^\w\s\áéíóúñ¿?!.,]', '', text)
        
        logger.debug(f"Cleaned text: {text}")
        return text
    
    def validate_text(self, text: str) -> Tuple[bool, str]:
        """
        Validate text input
        
        Args:
            text: Text to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not text:
            return False, "Text input is empty"
        
        if not isinstance(text, str):
            return False, "Input must be a string"
        
        cleaned = self.clean_text(text)
        
        if len(cleaned) == 0:
            return False, "Text becomes empty after cleaning"
        
        if len(cleaned) > self.max_length:
            return False, f"Text exceeds maximum length of {self.max_length} characters"
        
        return True, ""
    
    def process(self, text: str) -> Tuple[str, bool]:
        """
        Process and validate text in one step
        
        Args:
            text: Raw text from STT
            
        Returns:
            Tuple of (processed_text, is_valid)
        """
        is_valid, error_msg = self.validate_text(text)
        
        if not is_valid:
            logger.warning(f"Text validation failed: {error_msg}")
            return text, False
        
        cleaned = self.clean_text(text)
        logger.info(f"Text processed successfully: {cleaned}")
        return cleaned, True


# Global instance
text_processor = TextProcessor()
