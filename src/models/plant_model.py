from pydantic import BaseModel

class PlantIdentificationResponse(BaseModel):
    """
    Model for the plant identification response.

    TODO:
    - Add more fields to the response as needed.
    
    Placeholder:
    Contains basic identification information.
    """
    message: str
    plant_name: str = None
    scientific_name: str = None
    accuracy: float = None
