"""
Tests for Voice API
Basic test suite for voice conversation endpoint
"""
import os
import sys
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

# Add app directory to path
sys.path.insert(0, os.path.dirname(__file__) + "/../..")

from app.config import settings
from app.main import app


@pytest.fixture()
def client():
    with patch.object(settings, "validate", return_value=None):
        with TestClient(app) as test_client:
            yield test_client


class TestVoiceAPI:
    """Test cases for voice API endpoints"""

    def test_root_endpoint(self, client):
        """Test root endpoint exists"""
        response = client.get("/")
        assert response.status_code == 200
        assert "name" in response.json()
        assert "EduVoice" in response.json()["name"]

    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        with patch('app.voice.services.llm_service.llm_service.validate_api', return_value=True), patch(
            'app.voice.services.tts_service.tts_service.validate_api', return_value=True
        ):
            response = client.get("/health")

        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_voice_root_endpoint(self, client):
        """Test voice API root endpoint"""
        response = client.get("/api/voice/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "endpoints" in data

    def test_voice_process_success(self, client):
        """Test successful voice processing"""
        with patch('app.voice.services.llm_service.llm_service.query') as mock_llm, patch(
            'app.voice.services.tts_service.tts_service.synthesize'
        ) as mock_tts:
            mock_llm.return_value = {
                "status": "success",
                "response": "Para cambiar de programa debe contactar a registro.",
                "latency_ms": 500,
            }

            mock_tts.return_value = {
                "status": "success",
                "audio_data": "data:audio/mp3;base64,//NExAAeGJFJACAA...",
                "latency_ms": 1000,
            }

            payload = {
                "text": "¿Cómo cambio de programa académico?",
                "session_id": "test_session_123",
            }

            response = client.post("/api/voice/process", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "text_response" in data
        assert "audio_url" in data
        assert "latency_ms" in data
        assert data["text_response"] == "Para cambiar de programa debe contactar a registro."

    def test_voice_process_empty_text(self, client):
        """Test voice processing with empty text"""
        response = client.post("/api/voice/process", json={"text": ""})

        assert response.status_code == 422
        body = response.json()
        assert body["status"] == "error"
        assert body["error_code"] == "VALIDATION_ERROR"
        assert "text" in body["detail"].lower()

    def test_voice_process_too_long_text(self, client):
        """Test voice processing with text exceeding max length"""
        response = client.post("/api/voice/process", json={"text": "a" * 501})

        assert response.status_code == 422
        body = response.json()
        assert body["status"] == "error"
        assert body["error_code"] == "VALIDATION_ERROR"

    def test_voice_process_llm_error(self, client):
        """Test voice processing when LLM fails"""
        with patch('app.voice.services.llm_service.llm_service.query') as mock_llm:
            mock_llm.return_value = {
                "status": "error",
                "response": None,
                "error": "API error",
                "latency_ms": 500,
            }

            response = client.post("/api/voice/process", json={"text": "¿Cuáles son los requisitos?"})

        assert response.status_code == 500
        body = response.json()
        assert body["status"] == "error"
        assert body["error_code"] == "HTTP_ERROR"
        assert "LLM processing failed" in body["detail"]

    def test_health_endpoint_handles_degraded_service(self, client):
        with patch('app.voice.services.llm_service.llm_service.validate_api', return_value=True), patch(
            'app.voice.services.tts_service.tts_service.validate_api', return_value=False
        ):
            response = client.get("/api/voice/health")

        assert response.status_code == 503
        body = response.json()
        assert body["status"] == "degraded"
        assert body["services"]["llm"] == "ok"
        assert body["services"]["tts"] == "error"


class TestTextProcessor:
    """Test cases for text processor"""

    def test_text_processor_clean(self):
        """Test text cleaning"""
        from app.voice.services.text_processor import text_processor

        dirty_text = "  ¿Hola   mundo?  "
        cleaned = text_processor.clean_text(dirty_text)

        assert cleaned == "¿Hola mundo?"

    def test_text_processor_validate_empty(self):
        """Test validation of empty text"""
        from app.voice.services.text_processor import text_processor

        is_valid, error_msg = text_processor.validate_text("")

        assert not is_valid
        assert "empty" in error_msg.lower()

    def test_text_processor_validate_too_long(self):
        """Test validation of text exceeding max length"""
        from app.voice.services.text_processor import text_processor

        long_text = "a" * 501
        is_valid, error_msg = text_processor.validate_text(long_text)

        assert not is_valid
        assert "exceeds" in error_msg.lower()

    def test_text_processor_process_success(self):
        """Test successful text processing"""
        from app.voice.services.text_processor import text_processor

        text = "  ¿Hola mundo?  "
        processed, is_valid = text_processor.process(text)

        assert is_valid
        assert processed == "¿Hola mundo?"


class TestConfig:
    """Test cases for configuration"""

    def test_settings_validate_missing_keys(self):
        """Test that settings validation catches missing API keys"""
        from app.config import Settings

        settings_test = Settings()
        settings_test.GEMINI_API_KEY = ""

        with pytest.raises(ValueError):
            settings_test.validate()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
