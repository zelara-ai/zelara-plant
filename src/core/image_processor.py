from PIL import Image, UnidentifiedImageError
import io


def process_image(file_contents: bytes) -> bytes:
    """
    Processes the uploaded image.

    Args:
        file_contents (bytes): The uploaded image data.

    Returns:
        bytes: The processed image data.

    Raises:
        ValueError: If the image cannot be processed.
    """
    try:
        image = Image.open(io.BytesIO(file_contents))
        image = image.convert("RGB")  # Ensure image is in RGB mode
        # Resize the image to a maximum dimension if necessary
        max_size = (1500, 1500)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        return buffer.getvalue()
    except UnidentifiedImageError:
        raise ValueError("Uploaded file is not a valid image.")
    except Exception as e:
        # Handle other exceptions, possibly log the error
        print(f"Error processing image: {e}")
        raise ValueError("Error processing image.")
