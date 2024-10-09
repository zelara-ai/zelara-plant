import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys

# Mock external dependencies
sys.modules['kindwise'] = MagicMock()
sys.modules['kindwise.plant'] = MagicMock()

from src.main import app
from src.config import settings

client = TestClient(app)

@pytest.fixture
def mock_db_service():
    with patch('src.api.routes.DatabaseService') as MockDBService:
        mock_db = MockDBService.return_value
        yield mock_db

@pytest.fixture
def mock_identify_plant_task():
    with patch('src.api.routes.identify_plant_task') as mock_task:
        yield mock_task

@pytest.fixture
def mock_get_api_key_from_headers():
    with patch('src.config.get_api_key_from_headers') as mock_get_api_key:
        mock_get_api_key.return_value = 'mock-api-key'
        yield mock_get_api_key

def test_identify_plant_valid_image(mock_db_service, mock_identify_plant_task, mock_get_api_key_from_headers):
    mock_db_service.create_identification_record.return_value = '12345'

    # Simulate uploading a valid image
    with open('tests/ficus_lyrata_1152x1536.jpg', 'rb') as img_file:
        response = client.post(
            '/identify',
            files={'file': ('ficus.jpg', img_file, 'image/jpeg')}
        )

    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Plant identification is in progress.'
    assert data['identification_id'] == '12345'

    # Ensure the background task was added
    mock_identify_plant_task.assert_called_once()
    mock_db_service.create_identification_record.assert_called_once_with(status='Processing')

def test_identify_plant_invalid_file_type():
    # Attempt to upload a non-image file
    response = client.post(
        '/identify',
        files={'file': ('test.txt', b'Not an image', 'text/plain')}
    )
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == 'Invalid file format. Please upload an image.'

def test_identify_plant_empty_file():
    # Attempt to upload an empty image file
    response = client.post(
        '/identify',
        files={'file': ('empty.jpg', b'', 'image/jpeg')}
    )
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == 'Empty file.'

def test_identify_plant_base64_valid(mock_db_service, mock_identify_plant_task, mock_get_api_key_from_headers):
    mock_db_service.create_identification_record.return_value = '12345'
    # Base64-encoded image data
    with open('tests/ficus_lyrata_1152x1536.jpg', 'rb') as img_file:
        import base64
        image_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    response = client.post(
        '/identify_base64',
        json={'image_base64': image_base64}
    )

    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Plant identification is in progress.'
    assert data['identification_id'] == '12345'

    mock_identify_plant_task.assert_called_once()
    mock_db_service.create_identification_record.assert_called_once_with(status='Processing')

def test_identify_plant_base64_invalid():
    # Attempt to upload invalid base64 data
    response = client.post(
        '/identify_base64',
        json={'image_base64': 'invalid_base64_data'}
    )
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == 'Invalid base64-encoded image.'

def test_get_all_identifications(mock_db_service):
    mock_db_service.get_identifications.return_value = [
        {
            '_id': '12345',
            'status': 'Completed',
            'result': {
                'plant_name': 'Ficus lyrata',
                'common_names': ['Fiddle Leaf Fig'],
                'probability': 95.5,
                'taxonomy': {
                    'kingdom': 'Plantae',
                    'family': 'Moraceae',
                    'genus': 'Ficus',
                    'species': 'Ficus lyrata'
                },
                'identification_id': 'abc123',
                'is_plant': True,
                'created': '2024-09-15T12:00:00Z'
            }
        }
    ]

    response = client.get('/identifications')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['_id'] == '12345'
    assert data[0]['status'] == 'Completed'

def test_get_identification_by_id_found(mock_db_service):
    mock_db_service.get_identification_by_id.return_value = {
        '_id': '12345',
        'status': 'Completed',
        'result': {
            'plant_name': 'Ficus lyrata',
            'common_names': ['Fiddle Leaf Fig'],
            'probability': 95.5,
            'taxonomy': {
                'kingdom': 'Plantae',
                'family': 'Moraceae',
                'genus': 'Ficus',
                'species': 'Ficus lyrata'
            },
            'identification_id': 'abc123',
            'is_plant': True,
            'created': '2024-09-15T12:00:00Z'
        }
    }

    response = client.get('/identifications/12345')
    assert response.status_code == 200
    data = response.json()
    assert data['_id'] == '12345'
    assert data['status'] == 'Completed'

def test_get_identification_by_id_not_found(mock_db_service):
    mock_db_service.get_identification_by_id.return_value = None

    response = client.get('/identifications/99999')
    assert response.status_code == 404
    data = response.json()
    assert data['detail'] == 'Identification not found.'

# New Tests for Authentication Handling

def test_identify_plant_missing_api_key(mock_db_service, mock_identify_plant_task):
    mock_db_service.create_identification_record.return_value = '12345'

    # Simulate uploading a valid image without API key in PRODUCTION
    settings.environment = "PRODUCTION"
    with open('tests/ficus_lyrata_1152x1536.jpg', 'rb') as img_file:
        response = client.post(
            '/identify',
            files={'file': ('ficus.jpg', img_file, 'image/jpeg')}
            # No Authorization header provided
        )

    assert response.status_code == 401
    data = response.json()
    assert data['detail'] == 'API key not found in headers. Please provide the key in Authorization header.'

def test_identify_plant_invalid_api_key(mock_db_service, mock_identify_plant_task, mock_get_api_key_from_headers):
    mock_get_api_key_from_headers.return_value = 'invalid-api-key'
    mock_db_service.create_identification_record.return_value = '12345'

    # Simulate uploading a valid image with an invalid API key in PRODUCTION
    settings.environment = "PRODUCTION"
    with open('tests/ficus_lyrata_1152x1536.jpg', 'rb') as img_file:
        # Assuming that identify_plant_task raises an exception for invalid API keys
        mock_identify_plant_task.side_effect = Exception("Invalid API key")

        response = client.post(
            '/identify',
            files={'file': ('ficus.jpg', img_file, 'image/jpeg')},
            headers={'Authorization': 'Bearer invalid-api-key'}
        )

    assert response.status_code == 200  # The endpoint itself accepts the request and processes in background
    data = response.json()
    assert data['message'] == 'Plant identification is in progress.'
    assert data['identification_id'] == '12345'

    # Ensure the background task was added
    mock_identify_plant_task.assert_called_once()
    mock_db_service.create_identification_record.assert_called_once_with(status='Processing')
