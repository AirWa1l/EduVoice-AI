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
    """Service for LLM integration with Google Gemini API with Web Search capabilities"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize LLM Service with web search capabilities
        
        Args:
            api_key: Gemini API key (if not provided, uses config)
        """
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = "gemini-3-flash-preview"  # Fast, stable, and recommended for conversational AI
        self.timeout = settings.REQUEST_TIMEOUT
        
        # Configure Gemini API
        genai.configure(api_key=self.api_key)
        
        # Initialize base model
        self.model = genai.GenerativeModel(self.model_name)
        
        # Initialize model with web search capabilities using google_search tool
        try:
            self.model_with_search = genai.GenerativeModel(
                self.model_name,
                tools="google_search"
            )
        except Exception as e:
            logger.warning(f"Could not initialize web search model: {str(e)}. Falling back to regular model.")
            self.model_with_search = self.model
        
        # System prompt for academic guidance
        self.system_prompt = """Eres un asistente inteligente de voz para orientación académica en la Universidad del Valle. 
Tu objetivo es ayudar a estudiantes de la Universidad del Valle con preguntas sobre:
- Procesos académicos (inscripción, cambio de programa, solicitudes)
- Información general de la universidad
- Requisitos y trámites estudiantiles
- Orientación en temas académicos
- Fechas académicas, convocatorias y eventos importantes

IMPORTANTE - Búsqueda en Internet:
Si una pregunta requiere información actualizada (fechas, convocatorias, horarios, requisitos específicos actuales), 
DEBES usar la búsqueda en internet para obtener información precisa.
No inventes respuestas si no estás seguro. 
Si algo no lo sabes, admítelo y busca la información.

Responde de manera concisa, clara y útil en español.
Si la pregunta no está relacionada con temas académicos, indica amablemente que solo puedes ayudar con consultas académicas.
Mantén un tono profesional y amigable.
Las respuestas deben ser breves (máximo 3-4 oraciones) para ser reproducidas en voz."""
    
    def _should_use_web_search(self, text: str) -> bool:
        """
        Determine if a query needs web search
        
        Args:
            text: User query
            
        Returns:
            True if web search should be used, False otherwise
        """
        # Keywords that indicate need for web search
        search_keywords = [
            'fecha', 'fechas', 'cuándo', 'cuando',
            'horario', 'hora', 'próximo', 'proximo',
            'inscripción', 'inscripcion', 'convocatoria',
            'deadline', 'plazo', 'vigente', 'actual',
            'calendario', 'académico', 'academico',
            'requisito', 'requisitos', 'trámite', 'tramite',
            'proceso', 'procedimiento', '2026', '2025',
            'universidad del valle', 'univalle'
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in search_keywords)
    
    def query(self, text: str, session_id: Optional[str] = None) -> Dict:
        """
        Query the LLM with user input, using web search if needed
        
        Args:
            text: User input text
            session_id: Optional session ID for context
            
        Returns:
            Dictionary with response text and metadata
        """
        try:
            start_time = time.time()
            
            # Determine if we need web search
            use_search = self._should_use_web_search(text)
            
            # Select appropriate model
            model = self.model_with_search if use_search else self.model
            
            # Build the prompt
            prompt = f"{self.system_prompt}\n\nUsuario pregunta: {text}"
            
            # Generate response
            logger.info(f"Querying Gemini for text: {text[:50]}... (web_search={use_search})")
            
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=1024,
                )
            )
            
            # Extract response text
            response_text = response.text.strip()
            processing_time = (time.time() - start_time) * 1000  # ms
            
            logger.info(f"LLM response received in {processing_time:.2f}ms (used_web_search={use_search})")
            
            return {
                "status": "success",
                "response": response_text,
                "latency_ms": processing_time,
                "model": self.model_name,
                "used_web_search": use_search,
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
