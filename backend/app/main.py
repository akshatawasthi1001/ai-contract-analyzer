from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.db.health import check_database_connection


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(api_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": f"{settings.app_name} is running successfully!"
    }


@app.get("/health", tags=["Health"])
def health_check():
    database_status = check_database_connection()

    return {
        "status": "healthy" if database_status else "unhealthy",
        "database": "connected" if database_status else "disconnected",
    }