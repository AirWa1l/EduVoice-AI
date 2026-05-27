"""
EduVoice Backend - Main Application
FastAPI application for voice conversation processing
"""
import logging
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path

from app.config import settings
from app.voice.routes import router as voice_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def build_error_payload(message: str, error_code: str, detail: Optional[str] = None):
    return {
        "status": "error",
        "error_code": error_code,
        "message": message,
        "detail": detail or message,
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for app startup/shutdown"""
    # Startup
    logger.info("EduVoice API starting up...")
    try:
        settings.validate()
        logger.info("Configuration validated successfully")
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        raise
    yield
    # Shutdown
    logger.info("EduVoice API shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Voice conversation API for academic guidance",
    lifespan=lifespan
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    detail = exc.detail if isinstance(exc.detail, str) else "Request failed"
    logger.warning("HTTP error on %s: %s", request.url.path, detail)
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(build_error_payload(detail, "HTTP_ERROR", detail)),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first_error = exc.errors()[0] if exc.errors() else {}
    field = ".".join(str(part) for part in first_error.get("loc", ["body"]))
    detail = f"{field}: {first_error.get('msg', 'Invalid request')}"
    logger.warning("Validation error on %s: %s", request.url.path, detail)
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(
            build_error_payload("Request validation failed", "VALIDATION_ERROR", detail)
        ),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(
            build_error_payload(
                "Internal server error",
                "INTERNAL_ERROR",
                "An unexpected error occurred",
            )
        ),
    )

# Add CORS middleware with configurable origins
cors_origins = settings.CORS_ORIGINS if settings.CORS_ORIGINS else ["*"]

logger.info(f"CORS Origins configured: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for audio storage
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/audio", StaticFiles(directory=str(static_dir / "audio")), name="audio")

# Include routers
app.include_router(voice_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "documentation": "/docs"
    }


@app.get("/health")
async def health():
    """Basic health check"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )