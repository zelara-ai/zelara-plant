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
    # Verify that the image is in PNG format
    img = Image.open(BytesIO(processed_image))
    assert img.format == 'PNG'

def test_process_image_png():
    file_contents = create_test_image(format='PNG')
    processed_image = process_image(file_contents)
    assert isinstance(processed_image, bytes)
    assert len(processed_image) > 0
    img = Image.open(BytesIO(processed_image))
    assert img.format == 'PNG'

def test_process_image_gif():
    file_contents = create_test_image(format='GIF')
    processed_image = process_image(file_contents)
    assert isinstance(processed_image, bytes)
    assert len(processed_image) > 0
    img = Image.open(BytesIO(processed_image))
    assert img.format == 'PNG'

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

def test_process_image_aspect_ratio_too_low():
    # Aspect ratio = 0.5 (width=500, height=1000)
    img = Image.new('RGB', (500, 1000), 'blue')
    buf = BytesIO()
    img.save(buf, format='JPEG')
    buf.seek(0)
    file_contents = buf.getvalue()
    with pytest.raises(ValueError) as exc_info:
        process_image(file_contents)
    assert 'Invalid aspect ratio' in str(exc_info.value)

def test_process_image_aspect_ratio_too_high():
    # Aspect ratio = 2.0 (width=2000, height=1000)
    img = Image.new('RGB', (2000, 1000), 'green')
    buf = BytesIO()
    img.save(buf, format='JPEG')
    buf.seek(0)
    file_contents = buf.getvalue()
    with pytest.raises(ValueError) as exc_info:
        process_image(file_contents)
    assert 'Invalid aspect ratio' in str(exc_info.value)

def test_process_image_large_size():
    # Create a large image (5000x5000)
    file_contents = create_test_image(format='JPEG', size=(5000, 5000))
    processed_image = process_image(file_contents)
    img = Image.open(BytesIO(processed_image))
    assert img.size[0] <= 1500 and img.size[1] <= 1500
    assert img.format == 'PNG'
