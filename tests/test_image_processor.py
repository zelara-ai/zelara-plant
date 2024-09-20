import pytest
from io import BytesIO
from src.core.image_processor import process_image
from PIL import Image


def test_process_image_valid_jpeg():
    # Create an in-memory JPEG image
    img = Image.new("RGB", (100, 100), color="red")
    buf = BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    file_contents = buf.getvalue()

    processed_image = process_image(file_contents)
    assert isinstance(processed_image, bytes)
    assert len(processed_image) > 0


def test_process_image_valid_png():
    # Create an in-memory PNG image
    img = Image.new("RGBA", (2000, 2000), color="blue")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    file_contents = buf.getvalue()

    processed_image = process_image(file_contents)
    assert isinstance(processed_image, bytes)
    assert len(processed_image) > 0


def test_process_image_large():
    # Create a large image
    img = Image.new("RGB", (5000, 5000), color="green")
    buf = BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    file_contents = buf.getvalue()

    processed_image = process_image(file_contents)
    assert isinstance(processed_image, bytes)
    assert len(processed_image) > 0


def test_process_image_invalid_format():
    # Create a fake non-image file
    file_contents = b"This is not an image."
    with pytest.raises(ValueError) as exc_info:
        process_image(file_contents)
    assert "not a valid image" in str(exc_info.value)


def test_process_image_unsupported_format():
    # Create an image with an unsupported format (BMP)
    img = Image.new("RGB", (100, 100), color="red")
    buf = BytesIO()
    img.save(buf, format="BMP")  # BMP format is not supported in our code
    buf.seek(0)
    file_contents = buf.getvalue()

    with pytest.raises(ValueError) as exc_info:
        process_image(file_contents)
    assert "Unsupported image format" in str(exc_info.value)
