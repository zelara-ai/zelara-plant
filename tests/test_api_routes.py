import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys

# Mock 'kindwise' before importing app
sys.modules['kindwise'] = MagicMock()
sys.modules['kindwise.plant'] = MagicMock()

from src.main import app

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
def mock_kindwise_client():
    with patch('src.core.kindwise_wrapper.KindwiseClient') as MockKindwiseClient:
        mock_client = MockKindwiseClient.return_value
        # Set up a mock response for the identify_plant method
        mock_client.identify_plant.return_value = {
            'plant_name': 'Mocked Plant',
            'common_names': ['Mocked Common Name'],
            'probability': 99.9,
            'taxonomy': {
                'kingdom': 'Plantae',
                'family': 'Mocked Family',
                'genus': 'Mocked Genus',
                'species': 'Mocked Species'
            },
            'identification_id': 'mocked-id',
            'is_plant': True,
            'created': '2024-09-24T12:00:00Z'
        }
        yield mock_client

def test_identify_plant(mock_db_service, mock_kindwise_client):
    """
    Test the /identify endpoint with a valid image upload.
    """
    # Mock the database service
    mock_db_service.create_identification_record.return_value = '12345'

    # Simulate uploading an image
    with open('tests/ficus_lyrata_1152x1536.jpg', 'rb') as img_file:
        response = client.post(
            '/identify',
            files={'file': ('ficus.jpg', img_file, 'image/jpeg')}
        )

    assert response.status_code == 200
    data = response.json()
    assert 'identification_id' in data
    assert data['message'] == 'Plant identification is in progress.'
    assert data['identification_id'] == '12345'

    # Ensure the database record was created
    mock_db_service.create_identification_record.assert_called_once_with(status='Processing')

def test_identify_plant_invalid_image():
    """
    Test the /identify endpoint with an invalid image upload.
    """
    response = client.post(
        '/identify',
        files={'file': ('test.txt', b'Not an image', 'text/plain')}
    )
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == 'Invalid file format. Please upload an image.'

def test_identify_plant_empty_file():
    """
    Test the /identify endpoint with an empty file.
    """
    response = client.post(
        '/identify',
        files={'file': ('empty.jpg', b'', 'image/jpeg')}
    )
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == 'Empty file.'

def test_identify_plant_base64(mock_db_service, mock_kindwise_client):
    """
    Test the /identify_base64 endpoint with a valid base64 image.
    """
    # Mock the database service
    mock_db_service.create_identification_record.return_value = '12345'

    # Base64-encoded image data (truncated for brevity)
    image_base64 = 'iVBORw0KGgoAAAANSUhEUgAA...'

    response = client.post(
        '/identify_base64',
        json={'image_base64': image_base64}
    )

    assert response.status_code == 200
    data = response.json()
    assert 'identification_id' in data
    assert data['message'] == 'Plant identification is in progress.'
    assert data['identification_id'] == '12345'

    # Ensure the database record was created
    mock_db_service.create_identification_record.assert_called_once_with(status='Processing')

def test_identify_plant_base64_invalid_data():
    """
    Test the /identify_base64 endpoint with invalid base64 data.
    """
    response = client.post(
        '/identify_base64',
        json={'image_base64': 'not-valid-base64'}
    )
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == 'Invalid base64-encoded image.'

def test_get_all_identifications(mock_db_service):
    """
    Test the /identifications endpoint to retrieve all identifications.
    """
    mock_db_service.get_identifications.return_value = [
        {
            '_id': '123',
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
                'identification_id': 'some-id',
                'is_plant': True,
                'created': '2024-09-21T12:34:56Z'
            }
        }
    ]
    response = client.get('/identifications')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['status'] == 'Completed'
    assert data[0]['_id'] == '123'

def test_get_identification_by_id(mock_db_service):
    """
    Test the /identifications/{id} endpoint with a valid ID.
    """
    identification_id = '123'
    mock_db_service.get_identification_by_id.return_value = {
        '_id': identification_id,
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
            'identification_id': 'some-id',
            'is_plant': True,
            'created': '2024-09-21T12:34:56Z'
        }
    }
    response = client.get(f'/identifications/{identification_id}')
    assert response.status_code == 200
    data = response.json()
    assert data['_id'] == identification_id
    assert data['status'] == 'Completed'

def test_get_identification_by_id_not_found(mock_db_service):
    """
    Test the /identifications/{id} endpoint with an invalid ID.
    """
    identification_id = 'nonexistent'
    mock_db_service.get_identification_by_id.return_value = None
    response = client.get(f'/identifications/{identification_id}')
    assert response.status_code == 404
    data = response.json()
    assert data['detail'] == 'Identification not found.'
