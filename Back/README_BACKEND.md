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

### Voice API Endpoints (`/api/voice/`)

#### 1. POST `/api/voice/process` - Process Voice
**Endpoint principal para procesamiento de conversaciones por voz**

**Descripción:**
Recibe texto transcrito del frontend, lo procesa con un modelo de lenguaje (Google Gemini), y retorna una respuesta sintetizada en audio (Eleven Labs).

**Flujo de procesamiento:**
1. Recibe texto transcrito del frontend
2. Limpia y valida el texto
3. Procesa la consulta con LLM (Google Gemini API)
4. Sintetiza la respuesta a audio (Eleven Labs API)
5. Retorna el audio y texto de respuesta al frontend

**Request (application/json):**
```json
{
  "session_id": "session_12345",
  "text": "¿Cuáles son los requisitos para cambiar de programa académico?",
  "user_id": "user_67890"
}
```

**Parameters:**
- `session_id` (string): Identificador único de la sesión de conversación
- `text` (string): Texto transcrito por el usuario a procesar
- `user_id` (string): Identificador único del usuario

**Response (200 - Success, application/json):**
```json
{
  "status": "success",
  "text_response": "Para cambiar de programa académico, debe contactar a la oficina de registro...",
  "audio_url": "data:audio/mp3;base64,//NExAAeGJFJACAA...",
  "latency_ms": 3456.78,
  "timestamp": "2026-05-17T10:30:00"
}
```

**Response Fields:**
- `status` (string): Estado del procesamiento ("success", "error")
- `text_response` (string): Respuesta en texto generada por el LLM
- `audio_url` (string): URL o data URL con audio en formato MP3 (base64 encoded)
- `latency_ms` (float): Tiempo de procesamiento en milisegundos
- `timestamp` (string): Fecha y hora de procesamiento (ISO 8601)

**Error Codes:**
- `422 Validation Error`: Validación fallida en los parámetros enviados
- `500 Internal Server Error`: Error en el procesamiento (servicios LLM/TTS no disponibles)

---

#### 2. GET `/api/voice/health` - Health Check
**Verificación del estado de los servicios**

**Descripción:**
Valida que todos los servicios del backend estén operacionales. Verifica la conectividad con:
- Google Gemini API
- Eleven Labs API
- Base de datos (si aplica)

**Request:**
Sin parámetros

**Response (200 - Success, application/json):**
```json
{
  "status": "healthy",
  "services": {
    "gemini_api": "connected",
    "eleven_labs_api": "connected",
    "database": "connected"
  }
}
```

**Uso:**
- Monitoreo continuo de la disponibilidad del API
- Alertas de salud del sistema
- Verificación antes de procesar conversaciones

---

#### 3. GET `/api/voice/` - Voice Root
**Endpoint raíz de la API de voz**

**Descripción:**
Endpoint raíz que retorna información general sobre la API de voz.

**Request:**
Sin parámetros

**Response (200 - Success, application/json):**
```json
{
  "message": "Voice API Root - See /docs for API documentation",
  "version": "0.1.0"
}
```

---

### General Endpoints

#### 4. GET `/health` - Health Check General
**Verificación de salud general del backend**

Verifica que el servidor FastAPI esté corriendo correctamente.

---

#### 5. GET `/` - Root
**Endpoint raíz del backend**

Retorna información general del servidor.

---

## Modelos Pydantic

### VoiceRequest
Modelo para validar las solicitudes al endpoint `/api/voice/process`:

```python
class VoiceRequest(BaseModel):
    session_id: str  # Identificador de sesión único
    text: str        # Texto a procesar (mínimo 1 carácter)
    user_id: str     # Identificador del usuario
```

### VoiceResponse
Modelo para la respuesta del endpoint `/api/voice/process`:

```python
class VoiceResponse(BaseModel):
    status: str           # "success" o "error"
    text_response: str    # Respuesta generada por LLM
    audio_url: str        # Data URL con audio en base64
    latency_ms: float     # Tiempo de procesamiento
    timestamp: str        # Timestamp ISO 8601
```

---

## Arquitectura de Servicios

### LLM Service (`services/llm_service.py`)
- **Función**: Procesa texto usando Google Gemini API
- **Modelos soportados**: Gemini Pro
- **Salida**: Respuesta en texto contextualizada

### TTS Service (`services/tts_service.py`)
- **Función**: Sintetiza texto a audio usando Eleven Labs
- **Salida**: Audio en formato MP3 (base64 encoded)
- **Voces disponibles**: Configurables via `ELEVEN_LABS_VOICE_ID`

### Text Processor (`services/text_processor.py`)
- **Función**: Limpia, valida y preprocesa texto
- **Validaciones**: Largo mínimo, caracteres especiales, idioma

---

## Variables de Entorno Requeridas

```env
# Google Gemini API
GEMINI_API_KEY=tu_api_key_aqui

# Eleven Labs API
ELEVEN_LABS_API_KEY=tu_api_key_aqui
ELEVEN_LABS_VOICE_ID=voice_id_opcional  # Ej: "21m00Tcm4TlvDq8ikWAM"

# Configuración de servidor (opcional)
HOST=0.0.0.0
PORT=8000
DEBUG=False
```

---

## Testing

### Ejecutar tests
```bash
cd Back
pytest tests/ -v
```

### Probar endpoints manualmente
```bash
# Health check
curl http://localhost:8000/api/voice/health

# Procesar voz
curl -X POST http://localhost:8000/api/voice/process \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test_session",
    "text": "¿Cuál es la fecha del próximo parcial?",
    "user_id": "test_user"
  }'
```

---

## Documentación Interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

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
