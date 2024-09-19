import pytest
from fastapi import UploadFile
from io import BytesIO
from src.core.image_processor import process_image


def test_process_image_valid():
    # Create an in-memory image
    from PIL import Image

    img = Image.new("RGB", (100, 100), color="red")
    buf = BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    file = UploadFile(filename="test.jpg", file=buf, content_type="image/jpeg")
    processed_image = process_image(file)
    assert isinstance(processed_image, bytes)
    assert len(processed_image) > 0


def test_process_image_invalid():
    # Create a fake non-image file
    buf = BytesIO(b"This is not an image.")
    file = UploadFile(filename="test.txt", file=buf, content_type="text/plain")
    with pytest.raises(ValueError):
        process_image(file)
