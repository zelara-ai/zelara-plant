from fastapi import (
    APIRouter,
    BackgroundTasks,
    UploadFile,
    File,
    HTTPException,
    Request,
)
from typing import List
from src.core.task_manager import identify_plant_task
from src.models.plant_model import PlantIdentificationResponse, PlantIdentificationResult
from src.models.image_request import ImageUploadRequest
from src.db.db_service import DatabaseService
from src.config import settings, get_api_key_from_headers
import base64

router = APIRouter()

@router.post("/identify", response_model=PlantIdentificationResponse)
async def identify_plant(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    request: Request = None,
):
    """
    Endpoint to upload an image for plant identification.

    Args:
        background_tasks (BackgroundTasks): FastAPI background tasks.
        file (UploadFile): The uploaded image file.
        request (Request): The incoming request.

    Returns:
        PlantIdentificationResponse: The response containing the task ID.

    Raises:
        HTTPException: If the uploaded file is not an image or authentication fails.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, detail="Invalid file format. Please upload an image."
        )

    # Extract API key from headers if in PRODUCTION environment
    api_key = settings.kindwise_api_key
    if settings.environment == "PRODUCTION":
        try:
            api_key = get_api_key_from_headers(request.headers)
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))

    # Read the file contents
    file_contents = await file.read()
    if not file_contents:
        raise HTTPException(status_code=400, detail="Empty file.")

    # Start the identification task
    return await start_identification_task(background_tasks, file_contents, api_key)

@router.post("/identify_base64", response_model=PlantIdentificationResponse)
async def identify_plant_base64(
    background_tasks: BackgroundTasks,
    image_request: ImageUploadRequest,
    request: Request = None,
):
    """
    Endpoint to upload a base64-encoded image for plant identification.

    Args:
        background_tasks (BackgroundTasks): FastAPI background tasks.
        image_request (ImageUploadRequest): The request containing the base64 image.
        request (Request): The incoming request.

    Returns:
        PlantIdentificationResponse: The response containing the task ID.

    Raises:
        HTTPException: If the base64-encoded image is invalid or authentication fails.
    """
    # Extract API key from headers if in PRODUCTION environment
    api_key = settings.kindwise_api_key
    if settings.environment == "PRODUCTION":
        try:
            api_key = get_api_key_from_headers(request.headers)
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))

    # Decode the base64-encoded image
    try:
        image_data = base64.b64decode(image_request.image_base64)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid base64-encoded image.")

    if not image_data:
        raise HTTPException(status_code=400, detail="Empty image data.")

    # Start the identification task
    return await start_identification_task(background_tasks, image_data, api_key)

async def start_identification_task(background_tasks: BackgroundTasks, image_data: bytes, api_key: str):
    """
    Helper function to start the plant identification background task.

    Args:
        background_tasks (BackgroundTasks): FastAPI background tasks.
        image_data (bytes): The image data.
        api_key (str): The API key for Kindwise.

    Returns:
        PlantIdentificationResponse: The response containing the task ID.
    """
    # Initialize database service
    db_service = DatabaseService()

    # Create a new identification entry in the database with status 'Processing'
    identification_id = db_service.create_identification_record(status="Processing")

    # Submit the background task with the appropriate API key and identification ID
    background_tasks.add_task(
        identify_plant_task, image_data, api_key, identification_id
    )

    return PlantIdentificationResponse(
        message="Plant identification is in progress.",
        identification_id=str(identification_id),
    )

@router.get("/identifications", response_model=List[PlantIdentificationResult])
async def get_all_identifications():
    """
    Endpoint to retrieve all past plant identifications from the database.

    Returns:
        List[PlantIdentificationResult]: List of identification results.
    """
    db_service = DatabaseService()
    identifications = db_service.get_identifications()
    return identifications

@router.get("/identifications/{id}", response_model=PlantIdentificationResult)
async def get_identification_by_id(id: str):
    """
    Endpoint to retrieve a specific plant identification result by ID.

    Args:
        id (str): The identification ID.

    Returns:
        PlantIdentificationResult: The identification result.

    Raises:
        HTTPException: If the identification is not found.
    """
    db_service = DatabaseService()
    identification = db_service.get_identification_by_id(id)
    if identification is None:
        raise HTTPException(status_code=404, detail="Identification not found.")
    return identification
