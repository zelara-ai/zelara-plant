from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(
    title="Zelara Plant Worker",
    version="0.1.0",
    description="API for plant identification using Kindwise SDK."
)

# Include the API router
app.include_router(router)

@app.get("/")
async def root():
    """
    Root endpoint for health check.

    Returns:
        dict: Welcome message.
    """
    return {"message": "Welcome to the Zelara Plant Worker API"}
