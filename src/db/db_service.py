from pymongo import MongoClient
from src.config import settings

class DatabaseService:
    def __init__(self):
        """
        Initializes the database connection.

        - Connects to MongoDB based on environment settings.
        """
        self.client = MongoClient(settings.mongo_url)
        self.db = self.client.zelara_db
        self.collection = self.db.identifications

    def save_identification(self, data):
        """
        Saves plant identification data to the database.

        Args:
            data (dict): The identification result data.

        TODO:
            - Implement proper data insertion.
            - Handle duplicates or conflicts.
        """
        try:
            self.collection.insert_one(data)
            print("Identification saved to database.")
        except Exception as e:
            print(f"Error saving to database: {e}")

    def get_identifications(self):
        """
        Retrieves all plant identifications from the database.

        Returns:
            list: A list of identification documents.

        TODO:
            - Implement pagination if necessary.
            - Convert MongoDB documents to suitable response format.
        """
        try:
            return list(self.collection.find())
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

        TODO:
            - Implement proper data retrieval.
            - Handle cases where the ID is not found.
        """
        try:
            from bson.objectid import ObjectId
            return self.collection.find_one({"_id": ObjectId(id)})
        except Exception as e:
            print(f"Error fetching identification by ID: {e}")
            return None
