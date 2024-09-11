from PIL import Image
import io
from fastapi import UploadFile

def process_image(file: UploadFile) -> bytes:
    """
    Resize and process the uploaded image.

    TODO:
    - Resize the image to Kindwise API specifications.
    - Convert the image to a format suitable for the API (e.g., base64 or binary).
    
    Placeholder:
    Returns a mock processed image as binary data.
    """
    # TODO: Add image processing logic (resize, validate format)
    image = Image.open(file.file)
    image = image.resize((1500, 1500))  # Example resize logic

    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    
    return buffer.getvalue()
