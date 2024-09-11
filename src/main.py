from fastapi import FastAPI
from src.api.routes import router

app = FastAPI()

# Include the API router
app.include_router(router)

@app.get("/")
async def root():
    """
    Root endpoint for health check.
    
    Placeholder:
    Returns a welcome message.
    """
    return {"message": "Zelara Plant Worker API"}
