from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class PlantIdentificationResponse(BaseModel):
    """
    Model for the plant identification response.

    Attributes:
        message (str): Response message.
        identification_id (str): The ID of the identification task.
    """

    message: str
    identification_id: str


class PlantIdentificationResult(BaseModel):
    """
    Model for the plant identification result.

    Attributes:
        id (str): The identification ID.
        status (str): The status of the identification ('Processing', 'Completed', 'Error').
        result (Optional[PlantResult]): The identification result data.
        error_message (Optional[str]): Error message if any.
    """

    id: str = Field(alias="_id")
    status: str
    result: Optional["PlantResult"] = None
    error_message: Optional[str] = None


class PlantResult(BaseModel):
    plant_name: Optional[str]
    common_names: Optional[List[str]]
    probability: Optional[float]
    taxonomy: Optional[Dict[str, str]]
    identification_id: Optional[str]
    is_plant: Optional[bool]
    created: Optional[str]


PlantIdentificationResult.update_forward_refs()
