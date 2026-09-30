from fastapi import FastAPI

from backend.api.routes import router
from backend.api.documents import router as documents_router

from backend.auth.routes import router as auth_router
from backend.auth.models import init_database

from backend.config.settings import settings
from backend.utils.logger import get_logger
from backend.conversations.routes import router as conversations_router

logger = get_logger(__name__)


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0"
)



# Main API routes


app.include_router(
    router,
    prefix="/api"
)



# Authentication routes


app.include_router(
    auth_router,
    prefix="/api/auth"
)



# Document management routes


app.include_router(
    documents_router
)


app.include_router(
    conversations_router,
    prefix="/api"
)


# Application startup


@app.on_event("startup")
def startup_event():

    logger.info(
        "Starting Enterprise AI Assistant API..."
    )

    logger.info(
        f"Environment: {settings.ENVIRONMENT}"
    )

    # Initialize authentication database
    init_database()



# Root endpoint


@app.get("/")
def root():

    return {
        "message":
        "Enterprise AI Assistant API"
    }



# Health endpoint


@app.get("/health")
def health():

    return {

        "status":
        "healthy",

        "service":
        settings.APP_NAME,

        "environment":
        settings.ENVIRONMENT
    }