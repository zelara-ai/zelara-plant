import pytest
from unittest.mock import patch, MagicMock
from bson.objectid import ObjectId
from src.db.db_service import DatabaseService

@pytest.fixture
def mock_mongo_client():
    with patch('src.db.db_service.MongoClient') as MockMongoClient:
        mock_client = MockMongoClient.return_value
        yield mock_client

def test_create_identification_record(mock_mongo_client):
    mock_collection = mock_mongo_client.zelara_db.identifications
    mock_collection.insert_one.return_value.inserted_id = ObjectId('507f1f77bcf86cd799439011')

    db_service = DatabaseService()
    identification_id = db_service.create_identification_record(status='Processing')

    assert identification_id == '507f1f77bcf86cd799439011'
    mock_collection.insert_one.assert_called_once_with({'status': 'Processing'})

def test_update_identification(mock_mongo_client):
    mock_collection = mock_mongo_client.zelara_db.identifications
    db_service = DatabaseService()

    identification_id = '507f1f77bcf86cd799439011'
    data = {'plant_name': 'Ficus lyrata'}

    db_service.update_identification(identification_id, data)
    mock_collection.update_one.assert_called_once_with(
        {'_id': ObjectId(identification_id)},
        {'$set': {'status': 'Completed', 'result': data}}
    )

def test_update_identification_error(mock_mongo_client):
    mock_collection = mock_mongo_client.zelara_db.identifications
    db_service = DatabaseService()

    identification_id = '507f1f77bcf86cd799439011'
    error_message = 'An error occurred'

    db_service.update_identification_error(identification_id, error_message)
    mock_collection.update_one.assert_called_once_with(
        {'_id': ObjectId(identification_id)},
        {'$set': {'status': 'Error', 'error_message': error_message}}
    )

def test_get_identifications(mock_mongo_client):
    mock_collection = mock_mongo_client.zelara_db.identifications
    mock_collection.find.return_value = [
        {'_id': ObjectId('507f1f77bcf86cd799439011'), 'status': 'Completed', 'result': {}}
    ]

    db_service = DatabaseService()
    identifications = db_service.get_identifications()

    assert len(identifications) == 1
    assert identifications[0]['_id'] == '507f1f77bcf86cd799439011'

def test_get_identification_by_id_found(mock_mongo_client):
    mock_collection = mock_mongo_client.zelara_db.identifications
    mock_collection.find_one.return_value = {'_id': ObjectId('507f1f77bcf86cd799439011'), 'status': 'Completed'}

    db_service = DatabaseService()
    identification = db_service.get_identification_by_id('507f1f77bcf86cd799439011')

    assert identification['_id'] == '507f1f77bcf86cd799439011'

def test_get_identification_by_id_not_found(mock_mongo_client):
    mock_collection = mock_mongo_client.zelara_db.identifications
    mock_collection.find_one.return_value = None

    db_service = DatabaseService()
    identification = db_service.get_identification_by_id('nonexistent_id')

    assert identification is None
