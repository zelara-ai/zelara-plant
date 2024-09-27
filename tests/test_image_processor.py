import pytest
from io import BytesIO
from src.core.image_processor import process_image
from PIL import Image

def create_test_image(format='JPEG', size=(100, 100), color='red'):
    img = Image.new('RGB', size, color)
    buf = BytesIO()
    img.save(buf, format=format)
    buf.seek(0)
    return buf.getvalue()

def test_process_image_jpeg():
    file_contents = create_test_image(format='JPEG')
    processed_image = process_image(file_contents)
    assert isinstance(processed_image, bytes)
    assert len(processed_image) > 0

def test_process_image_png():
    file_contents = create_test_image(format='PNG')
    processed_image = process_image(file_contents)
    assert isinstance(processed_image, bytes)
    assert len(processed_image) > 0

def test_process_image_unsupported_format():
    file_contents = create_test_image(format='BMP')
    with pytest.raises(ValueError) as exc_info:
        process_image(file_contents)
    assert 'Unsupported image format' in str(exc_info.value)

def test_process_image_invalid_data():
    file_contents = b'Not an image'
    with pytest.raises(ValueError) as exc_info:
        process_image(file_contents)
    assert 'Uploaded file is not a valid image' in str(exc_info.value)

def test_process_image_large_image():
    file_contents = create_test_image(size=(5000, 5000))
    processed_image = process_image(file_contents)
    img = Image.open(BytesIO(processed_image))
    assert img.size <= (1500, 1500)
