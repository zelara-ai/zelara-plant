from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str = "LOCAL"
    mongo_url: str
    kindwise_api_key: str = None

    class Config:
        env_file = ".env"

settings = Settings()

def get_api_key_from_headers(headers) -> str:
    """
    Retrieve the API key from request headers.

    Args:
        headers (dict): The request headers.

    Returns:
        str: The extracted API key.

    Raises:
        ValueError: If the API key is not found in the headers.
    """
    if "Authorization" in headers:
        return headers["Authorization"].replace("Bearer ", "")
    raise ValueError("API key not found in headers. Please provide the key in Authorization header.")
