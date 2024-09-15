from pydantic import BaseModel

class PlantIdentificationResponse(BaseModel):
    """
    Model for the plant identification response.

    Attributes:
        message (str): Response message.
        plant_name (str): Common name of the plant.
        scientific_name (str): Scientific name of the plant.
        accuracy (float): Confidence level of the identification.

    TODO:
        - Add more fields as required by the identification result.
    """
    message: str
    plant_name: str = None
    scientific_name: str = None
    accuracy: float = None
