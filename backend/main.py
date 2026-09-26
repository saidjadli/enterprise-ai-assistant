from fastapi import FastAPI

from backend.api.routes import router

from backend.config.settings import settings

from backend.utils.logger import get_logger



logger = get_logger(__name__)



app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0"
)



app.include_router(
    router,
    prefix="/api"
)



@app.on_event("startup")
def startup_event():

    logger.info(
        "Starting Enterprise AI Assistant API..."
    )

    logger.info(
        f"Environment: {settings.ENVIRONMENT}"
    )



@app.get("/")
def root():

    return {
        "message":
        "Enterprise AI Assistant API"
    }



@app.get("/health")
def health():

    return {

        "status": "healthy",

        "service":
        settings.APP_NAME,

        "environment":
        settings.ENVIRONMENT

    }