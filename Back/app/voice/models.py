"""
Pydantic models for voice processing API
Defines request/response schemas
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class VoiceRequest(BaseModel):
    """Request model for voice processing endpoint"""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "text": "¿Cuáles son los requisitos para cambiar de programa académico?",
            "session_id": "session_12345",
            "user_id": "user_67890"
        }
    })
    
    text: str = Field(
        ..., 
        min_length=1, 
        max_length=500,
        description="User's transcribed text from voice input"
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Session ID for context management (optional)"
    )
    user_id: Optional[str] = Field(
        default=None,
        description="User ID for personalization (optional)"
    )


class VoiceResponse(BaseModel):
    """Response model for voice processing endpoint"""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "text_response": "Para cambiar de programa académico, debe contactar a la oficina de registro...",
            "audio_url": "data:audio/mp3;base64,//NExAAeGJFJACAA...",
            "status": "success",
            "error_message": None,
            "latency_ms": 3456.78,
            "timestamp": "2026-05-17T10:30:00"
        }
    })
    
    text_response: str = Field(
        ..., 
        description="LLM-generated text response"
    )
    audio_url: str = Field(
        ...,
        description="URL or base64 encoded audio file"
    )
    status: str = Field(
        default="success",
        description="Status of the request (success, error)"
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if status is error"
    )
    latency_ms: float = Field(
        ...,
        description="Total processing time in milliseconds"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp"
    )


class ErrorResponse(BaseModel):
    """Error response model"""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "status": "error",
            "error_code": "TEXT_TOO_LONG",
            "message": "Input text exceeds maximum length of 500 characters",
            "timestamp": "2026-05-17T10:30:00"
        }
    })
    
    status: str = "error"
    error_code: str = Field(..., description="Error code identifier")
    message: str = Field(..., description="Detailed error message")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
