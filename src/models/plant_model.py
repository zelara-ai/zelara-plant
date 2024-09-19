from pydantic import BaseModel, Field
from typing import Optional, Any


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
        result (Optional[Any]): The identification result data.
        error_message (Optional[str]): Error message if any.
    """

    id: str = Field(alias="_id")
    status: str
    result: Optional[Any] = None
    error_message: Optional[str] = None
