from fastapi import FastAPI, Request, HTTPException
from src.config import settings, get_api_key_from_headers
from src.api.routes import router

app = FastAPI(
    title="Zelara Plant Worker",
    version="1.0.0",
    description="API for plant identification using Kindwise SDK."
)

@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    if settings.environment == "PRODUCTION":
        try:
            api_key = get_api_key_from_headers(request.headers)
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))
    return await call_next(request)

app.include_router(router)

@app.get("/")
async def root():
    """
    Root endpoint for health check.

    Returns:
        dict: Welcome message.
    """
    return {"message": "Welcome to the Zelara Plant Worker API"}
