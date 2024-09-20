from pydantic import BaseModel

class ImageUploadRequest(BaseModel):
    image_base64: str
