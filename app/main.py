from fastapi import FastAPI
from app.infrastructure.controllers import router

app = FastAPI(
    title="Simple DDD API",
    description="Una aplicación simple usando Domain Driven Design",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Bienvenido a la API con DDD"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return {"message": "No favicon configured"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 