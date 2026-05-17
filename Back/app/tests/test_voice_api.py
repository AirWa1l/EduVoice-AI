"""
Tests for Voice API
Basic test suite for voice conversation endpoint
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.dirname(__file__) + "/..")

from main import app

client = TestClient(app)


class TestVoiceAPI:
    """Test cases for voice API endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint exists"""
        response = client.get("/")
        assert response.status_code == 200
        assert "name" in response.json()
        assert "EduVoice" in response.json()["name"]
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_voice_root_endpoint(self):
        """Test voice API root endpoint"""
        response = client.get("/api/voice/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "endpoints" in data
    
    @patch('voice.services.llm_service.llm_service.query')
    @patch('voice.services.tts_service.tts_service.synthesize')
    def test_voice_process_success(self, mock_tts, mock_llm):
        """Test successful voice processing"""
        # Mock LLM response
        mock_llm.return_value = {
            "status": "success",
            "response": "Para cambiar de programa debe contactar a registro.",
            "latency_ms": 500
        }
        
        # Mock TTS response
        mock_tts.return_value = {
            "status": "success",
            "audio_data": "data:audio/mp3;base64,//NExAAeGJFJACAA...",
            "latency_ms": 1000
        }
        
        # Make request
        payload = {
            "text": "¿Cómo cambio de programa académico?",
            "session_id": "test_session_123"
        }
        
        response = client.post("/api/voice/process", json=payload)
        
        # Assert response
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "text_response" in data
        assert "audio_url" in data
        assert "latency_ms" in data
        assert data["text_response"] == "Para cambiar de programa debe contactar a registro."
    
    def test_voice_process_empty_text(self):
        """Test voice processing with empty text"""
        payload = {
            "text": "",
        }
        
        response = client.post("/api/voice/process", json=payload)
        
        # Should fail validation
        assert response.status_code == 422  # Pydantic validation error
    
    def test_voice_process_too_long_text(self):
        """Test voice processing with text exceeding max length"""
        # Create text longer than 500 characters
        long_text = "a" * 501
        
        payload = {
            "text": long_text,
        }
        
        response = client.post("/api/voice/process", json=payload)
        
        # Should fail validation
        assert response.status_code == 422
    
    @patch('voice.services.llm_service.llm_service.query')
    def test_voice_process_llm_error(self, mock_llm):
        """Test voice processing when LLM fails"""
        # Mock LLM error
        mock_llm.return_value = {
            "status": "error",
            "response": None,
            "error": "API error",
            "latency_ms": 500
        }
        
        payload = {
            "text": "¿Cuáles son los requisitos?"
        }
        
        response = client.post("/api/voice/process", json=payload)
        
        # Should return error
        assert response.status_code == 500


class TestTextProcessor:
    """Test cases for text processor"""
    
    def test_text_processor_clean(self):
        """Test text cleaning"""
        from voice.services.text_processor import text_processor
        
        dirty_text = "  ¿Hola   mundo?  "
        cleaned = text_processor.clean_text(dirty_text)
        
        assert cleaned == "¿Hola mundo?"
    
    def test_text_processor_validate_empty(self):
        """Test validation of empty text"""
        from voice.services.text_processor import text_processor
        
        is_valid, error_msg = text_processor.validate_text("")
        
        assert not is_valid
        assert "empty" in error_msg.lower()
    
    def test_text_processor_validate_too_long(self):
        """Test validation of text exceeding max length"""
        from voice.services.text_processor import text_processor
        
        long_text = "a" * 501
        is_valid, error_msg = text_processor.validate_text(long_text)
        
        assert not is_valid
        assert "exceeds" in error_msg.lower()
    
    def test_text_processor_process_success(self):
        """Test successful text processing"""
        from voice.services.text_processor import text_processor
        
        text = "  ¿Hola mundo?  "
        processed, is_valid = text_processor.process(text)
        
        assert is_valid
        assert processed == "¿Hola mundo?"


class TestConfig:
    """Test cases for configuration"""
    
    def test_settings_validate_missing_keys(self):
        """Test that settings validation catches missing API keys"""
        from config import Settings
        
        settings_test = Settings()
        settings_test.GEMINI_API_KEY = ""
        
        with pytest.raises(ValueError):
            settings_test.validate()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
