from PIL import Image, UnidentifiedImageError
import io

# Configure logging
SUPPORTED_FORMATS = ["JPEG", "PNG", "GIF"]
MAX_SIZE = (1500, 1500)
JPEG_QUALITY = 85


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
        # Load an image from the provided bytes.
        image = Image.open(io.BytesIO(file_contents))

        # Validate the image format.
        if image.format not in SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported image format: {image.format}. Please upload a JPEG, PNG, or GIF image.")
        
        # Processe the image by converting it to RGB and resizing.
        image = image.convert("RGB")
        image.thumbnail(MAX_SIZE, Image.LANCZOS)

        # Save the processed image to a bytes object.
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=JPEG_QUALITY, optimize=True)

        return buffer.getvalue()

    except UnidentifiedImageError as e:
        raise ValueError(f"Uploaded file is not a valid image or is corrupted. {str(e)}")
    except ValueError as ve:
        raise ve
    except Exception as e:
        print(f"Error processing image: {e}")
        raise ValueError("Error processing image.")
