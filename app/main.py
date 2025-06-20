import logging
import os
from fastapi import FastAPI
from infrastructure.controllers import router

# Configure loggin
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Simple DDD API",
    description="Una aplicación simple usando Domain Driven Design",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Bienvenido a la API con DDD", "status": "healthy"}


@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {
        "status": "healthy",
        "service": "Simple DDD API",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return {"message": "No favicon configured"}


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting application...")
    uvicorn.run(app, host="0.0.0.0", port=8000) 