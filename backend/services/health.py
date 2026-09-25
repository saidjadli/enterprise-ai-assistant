from backend.config.settings import settings


def health_check():

    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.version,
        "environment": settings.environment
    }