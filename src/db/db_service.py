from pymongo import MongoClient
from src.config import settings
from bson.objectid import ObjectId


class DatabaseService:
    def __init__(self):
        """
        Initializes the database connection.

        - Connects to MongoDB based on environment settings.
        """
        self.client = MongoClient(settings.mongo_url)
        self.db = self.client.zelara_db
        self.collection = self.db.identifications

    def create_identification_record(self, status: str = "Processing"):
        """
        Creates a new identification record in the database.

        Args:
            status (str): The initial status of the identification.

        Returns:
            str: The ID of the new identification record.
        """
        identification = {"status": status}
        result = self.collection.insert_one(identification)
        return str(result.inserted_id)

    def update_identification(self, identification_id: str, data: dict):
        """
        Updates an existing identification record with the result data.

        Args:
            identification_id (str): The ID of the identification record.
            data (dict): The identification result data.
        """
        try:
            self.collection.update_one(
                {"_id": ObjectId(identification_id)},
                {"$set": {"status": "Completed", "result": data}},
            )
            print("Identification updated in database.")
        except Exception as e:
            print(f"Error updating database: {e}")

    def update_identification_error(self, identification_id: str, error_message: str):
        """
        Updates an existing identification record with an error status.

        Args:
            identification_id (str): The ID of the identification record.
            error_message (str): The error message.
        """
        try:
            self.collection.update_one(
                {"_id": ObjectId(identification_id)},
                {"$set": {"status": "Error", "error_message": error_message}},
            )
            print("Identification error updated in database.")
        except Exception as e:
            print(f"Error updating database with error: {e}")

    def get_identifications(self):
        """
        Retrieves all plant identifications from the database.

        Returns:
            list: A list of identification documents.
        """
        try:
            identifications = self.collection.find()
            return [self._serialize_identification(ident) for ident in identifications]
        except Exception as e:
            print(f"Error fetching identifications: {e}")
            return []

    def get_identification_by_id(self, id: str):
        """
        Retrieves a specific plant identification by ID.

        Args:
            id (str): The identification ID.

        Returns:
            dict: The identification document.
        """
        try:
            identification = self.collection.find_one({"_id": ObjectId(id)})
            if identification:
                return self._serialize_identification(identification)
            else:
                return None
        except Exception as e:
            print(f"Error fetching identification by ID: {e}")
            return None

    def _serialize_identification(self, identification):
        """
        Serializes the identification document for JSON response.

        Args:
            identification (dict): The identification document.

        Returns:
            dict: The serialized identification.
        """
        identification["_id"] = str(identification["_id"])
        return identification
