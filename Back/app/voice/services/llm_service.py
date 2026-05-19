"""
LLM Service - Integration with Google Gemini API
Handles natural language processing for academic guidance
"""
import logging
import google.generativeai as genai
from typing import Optional, Dict
from app.config import settings
import time

logger = logging.getLogger(__name__)


class LLMService:
    """Service for LLM integration with Google Gemini API"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize LLM Service
        
        Args:
            api_key: Gemini API key (if not provided, uses config)
        """
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = "gemini-3-flash-preview"
        self.timeout = settings.REQUEST_TIMEOUT
        
        # Configure Gemini API
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        
        # System prompt for academic guidance
        self.system_prompt = """Eres un asistente inteligente de voz para orientación académica en la Universidad del Valle.
Tu objetivo es ayudar a estudiantes de la Universidad del Valle con preguntas sobre:
- Procesos académicos (inscripción, cambio de programa, solicitudes)
- Información general de la universidad
- Requisitos y trámites estudiantiles
- Orientación en temas académicos

IMPORTANTE:
- Responde en español, de manera clara y concisa
- Las respuestas deben ser breves (máximo 3-4 oraciones) para reproducción en voz
- Si necesitas información que no conoces con certeza, di: "Te recomiendo verificar esta información en el sitio oficial de la Universidad del Valle"
- Proporciona referencias cuando sea posible
- Mantén un tono profesional y amigable

Si la pregunta no está relacionada con temas académicos, indica amablemente que solo puedes ayudar con consultas sobre la Universidad del Valle."""
    
    def query(self, text: str, session_id: Optional[str] = None) -> Dict:
        """
        Query the LLM with user input
        
        Args:
            text: User input text
            session_id: Optional session ID for context
            
        Returns:
            Dictionary with response text and metadata
        """
        try:
            start_time = time.time()
            
            # Build the prompt
            prompt = f"{self.system_prompt}\n\nUsuario pregunta: {text}"
            
            # Generate response
            logger.info(f"Querying Gemini for text: {text[:50]}...")
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=1024,
                )
            )
            
            # Extract response text
            response_text = response.text.strip()
            processing_time = (time.time() - start_time) * 1000  # ms
            
            logger.info(f"LLM response received in {processing_time:.2f}ms")
            
            return {
                "status": "success",
                "response": response_text,
                "latency_ms": processing_time,
                "model": self.model_name,
                "session_id": session_id
            }
        
        except Exception as e:
            logger.error(f"LLM query error: {str(e)}")
            return {
                "status": "error",
                "response": None,
                "error": str(e),
                "latency_ms": (time.time() - start_time) * 1000
            }
    
    def validate_api(self) -> bool:
        """
        Validate that API connection works
        
        Returns:
            True if API is reachable, False otherwise
        """
        try:
            test_response = self.model.generate_content("Hola")
            return test_response.text is not None
        except Exception as e:
            logger.error(f"API validation failed: {str(e)}")
            return False


# Global instance
llm_service = LLMService()
