# EduVoice Backend - Voice Conversation API

## Descripción
Backend FastAPI para procesamiento de conversaciones inteligentes por voz. Implementa el flujo completo:
- **STT**: Recibe texto transcrito del frontend (Web Speech API)
- **LLM**: Procesa consultas con Google Gemini API
- **TTS**: Convierte respuestas a audio con Eleven Labs

## Stack Tecnológico
- **Framework**: FastAPI 0.136.1
- **Server**: Uvicorn
- **LLM**: Google Gemini API
- **TTS**: Eleven Labs API
- **Testing**: pytest
- **Validación**: Pydantic

## Estructura del Proyecto

```
Back/
├── app/
│   ├── main.py                    # FastAPI application
│   ├── config.py                  # Configuration and settings
│   │
│   ├── voice/                     # Voice processing module
│   │   ├── __init__.py
│   │   ├── models.py              # Pydantic models (VoiceRequest, VoiceResponse)
│   │   ├── routes.py              # API endpoints
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── llm_service.py     # Google Gemini integration
│   │       ├── tts_service.py     # Eleven Labs integration
│   │       └── text_processor.py  # Text cleaning and validation
│   │
│   ├── tests/                     # Test suite
│   │   ├── __init__.py
│   │   └── test_voice_api.py      # API tests
│   │
│   └── utils/                     # Utility functions (expandable)
│       └── __init__.py
│
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── Dockerfile                     # Container image (pendiente)
└── docker-compose.yml             # Services orchestration (pendiente)
```

## Instalación

### 1. Clonar el repositorio
```bash
git clone <repo-url>
cd EduVoice-AI
```

### 2. Crear variable de entorno
```bash
cd Back
cp .env.example .env
# Editar .env y agregar tus API keys
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar API Keys

#### Google Gemini API
1. Ve a https://ai.google.dev/
2. Crea una API key
3. Copia la key a `.env` como `GEMINI_API_KEY`

#### Eleven Labs
1. Ve a https://elevenlabs.io/
2. Regístrate y obtén una API key
3. Copia la key a `.env` como `ELEVEN_LABS_API_KEY`
4. (Opcional) Selecciona un voice ID y cópalo a `ELEVEN_LABS_VOICE_ID`

## Ejecución

### Desarrollo Local
```bash
cd Back
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

La aplicación estará disponible en:
- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Con Docker (Pendiente)
```bash
docker-compose up backend
```

## Endpoints

### POST /api/voice/process
Procesa una consulta de voz completa

**Request:**
```json
{
  "text": "¿Cuáles son los requisitos para cambiar de programa?",
  "session_id": "session_123",
  "user_id": "user_456"
}
```

**Response:**
```json
{
  "text_response": "Para cambiar de programa académico, debe contactar a la oficina de registro y presentar...",
  "audio_url": "data:audio/mp3;base64,//NExAAeGJFJACAA...",
  "status": "success",
  "error_message": null,
  "latency_ms": 3456.78,
  "timestamp": "2026-05-17T10:30:00"
}
```

### GET /api/voice/health
Verifica que todos los servicios estén operacionales

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "llm": "ok",
    "tts": "ok"
  }
}
```

### GET /api/voice/
Información general de la API

## Testing

### Ejecutar todos los tests
```bash
pytest app/tests/ -v
```

### Ejecutar tests con cobertura
```bash
pytest app/tests/ --cov=app --cov-report=html
```

### Test específico
```bash
pytest app/tests/test_voice_api.py::TestVoiceAPI::test_voice_process_success -v
```

## Componentes Principales

### TextProcessor (`voice/services/text_processor.py`)
- Limpia y valida texto de entrada
- Elimina caracteres especiales
- Verifica longitud máxima
- Normaliza espacios en blanco

### LLMService (`voice/services/llm_service.py`)
- Integración con Google Gemini API
- Contexto especializado para orientación académica
- Manejo de errores de API
- Validación de conexión

### TTSService (`voice/services/tts_service.py`)
- Integración con Eleven Labs API
- Conversión de texto a audio (mpeg)
- Codificación en base64 para transmisión
- Manejo de timeouts y errores

### VoiceRouter (`voice/routes.py`)
- Endpoint POST /api/voice/process
- Orquesta los 3 servicios (text → LLM → TTS)
- Medición de latencia
- Manejo de errores integral

## Flujo de Procesamiento

```
1. Frontend envía texto transcrito → POST /api/voice/process
   ↓
2. TextProcessor: Limpia y valida
   ↓
3. LLMService: Consulta Gemini API
   ↓
4. TTSService: Sintetiza audio
   ↓
5. Response: {text, audio, latency, status}
   ↓
6. Frontend: Muestra texto + reproduce audio
```

## Métricas Medidas

- **Latencia Total**: Tiempo end-to-end
- **Latencia LLM**: Tiempo de respuesta de Gemini
- **Latencia TTS**: Tiempo de síntesis de voz
- **Bytes de Audio**: Tamaño del archivo generado

## Manejo de Errores

La API retorna códigos HTTP estándar:
- **200**: Éxito
- **400**: Validación fallida (texto inválido)
- **500**: Error del servidor (API externa)
- **503**: Servicio no disponible

## Siguientes Pasos (Sprint 2)

- [ ] Optimización de latencia
- [ ] Context management (sesiones)
- [ ] Prompt engineering avanzado
- [ ] Rate limiting
- [ ] Caching de respuestas
- [ ] Logging detallado
- [ ] Tests adicionales (objetivo: 50% cobertura)
- [ ] Documentación OpenAPI completa
- [ ] Despliegue en cloud (Render/Railway)

## Referencias

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Google Gemini API](https://ai.google.dev/tutorials/python_quickstart)
- [Eleven Labs API](https://elevenlabs.io/docs/api-reference)
- [Pydantic](https://docs.pydantic.dev/)

## Contribuidores

- **Daniel Rojas Barreneche** - Backend Developer

---

**Rama**: `feature/voice-conversation-endpoint`  
**Estado**: Sprint 1 - En Desarrollo  
**Última actualización**: 17 de mayo de 2026
