from PIL import Image, UnidentifiedImageError
import io

# Configure logging
SUPPORTED_FORMATS = ["JPEG", "PNG", "GIF"]
MAX_SIZE = (1500, 1500)
JPEG_QUALITY = 85
ASPECT_RATIO_RANGE = (0.8, 1.2)

def process_image(file_contents: bytes) -> bytes:
    """
    Processes the uploaded image by validating aspect ratio, resizing, and applying lossless compression.

    Args:
        file_contents (bytes): The uploaded image data.

    Returns:
        bytes: The processed image data in PNG format.

    Raises:
        ValueError: If the image cannot be processed or fails validation.
    """
    try:
        # Load an image from the provided bytes.
        image = Image.open(io.BytesIO(file_contents))

        # Validate the image format.
        if image.format not in SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported image format: {image.format}. Please upload a JPEG, PNG, or GIF image."
            )

        # Validate aspect ratio
        width, height = image.size
        aspect_ratio = width / height
        if not (ASPECT_RATIO_RANGE[0] <= aspect_ratio <= ASPECT_RATIO_RANGE[1]):
            raise ValueError(
                f"Invalid aspect ratio: {aspect_ratio:.2f}. "
                f"Please upload an image with an aspect ratio between {ASPECT_RATIO_RANGE[0]} and {ASPECT_RATIO_RANGE[1]}."
            )

        # Convert image to RGB if not already
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Resize the image while maintaining aspect ratio
        image.thumbnail(MAX_SIZE, Image.LANCZOS)

        # Save the processed image to a bytes object using lossless compression (PNG)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG", optimize=True)
        buffer.seek(0)

        return buffer.getvalue()

    except UnidentifiedImageError as e:
        raise ValueError(f"Uploaded file is not a valid image or is corrupted. {str(e)}")
    except ValueError as ve:
        raise ve
    except Exception as e:
        print(f"Error processing image: {e}")
        raise ValueError("Error processing image.")
