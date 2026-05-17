"""
Voice API Routes
Defines endpoints for voice conversation processing
"""
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import logging
import time
import uuid

from voice.models import VoiceRequest, VoiceResponse, ErrorResponse
from voice.services.text_processor import text_processor
from voice.services.llm_service import llm_service
from voice.services.tts_service import tts_service
from config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/voice", tags=["voice"])


@router.post("/process", response_model=VoiceResponse)
async def process_voice(request: VoiceRequest):
    """
    Main endpoint for voice conversation processing
    
    Flow:
    1. Receive transcribed text from frontend
    2. Clean and validate text
    3. Process with LLM (Gemini)
    4. Synthesize response to speech (Eleven Labs)
    5. Return audio and text to frontend
    
    Args:
        request: VoiceRequest with text, session_id, user_id
        
    Returns:
        VoiceResponse with text_response, audio_url, status
        
    Raises:
        HTTPException: If processing fails
    """
    start_time = time.time()
    
    try:
        logger.info(f"Processing voice request: {request.text[:50]}...")
        
        # Step 1: Clean and validate text
        processed_text, is_valid = text_processor.process(request.text)
        
        if not is_valid:
            logger.warning(f"Text validation failed: {request.text}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid input text"
            )
        
        # Step 2: Query LLM
        llm_result = llm_service.query(processed_text, request.session_id)
        
        if llm_result.get("status") != "success":
            logger.error(f"LLM query failed: {llm_result.get('error')}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="LLM processing failed"
            )
        
        llm_response = llm_result.get("response", "")
        
        # Step 3: Synthesize to speech
        tts_result = tts_service.synthesize(llm_response)
        
        if tts_result.get("status") != "success":
            logger.error(f"TTS synthesis failed: {tts_result.get('error')}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="TTS synthesis failed"
            )
        
        audio_url = tts_result.get("audio_data", "")
        
        # Calculate total latency
        total_latency = (time.time() - start_time) * 1000  # ms
        
        logger.info(f"Voice processing completed in {total_latency:.2f}ms")
        
        # Return response
        return VoiceResponse(
            text_response=llm_response,
            audio_url=audio_url,
            status="success",
            error_message=None,
            latency_ms=total_latency
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in voice processing: {str(e)}")
        total_latency = (time.time() - start_time) * 1000
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Voice processing error: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    Validates that all services are operational
    
    Returns:
        Status of backend services
    """
    try:
        llm_ok = llm_service.validate_api()
        tts_ok = tts_service.validate_api()
        
        status_code = status.HTTP_200_OK if (llm_ok and tts_ok) else status.HTTP_503_SERVICE_UNAVAILABLE
        
        return JSONResponse(
            status_code=status_code,
            content={
                "status": "healthy" if (llm_ok and tts_ok) else "degraded",
                "services": {
                    "llm": "ok" if llm_ok else "error",
                    "tts": "ok" if tts_ok else "error"
                }
            }
        )
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )


@router.get("/")
async def voice_root():
    """Root endpoint for voice API"""
    return {
        "name": "EduVoice - Voice Conversation API",
        "version": settings.APP_VERSION,
        "endpoints": {
            "process": "POST /api/voice/process - Process voice conversation",
            "health": "GET /api/voice/health - Health check"
        }
    }
