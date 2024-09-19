from src.core.image_processor import process_image
from src.core.kindwise_wrapper import KindwiseClient
from src.db.db_service import DatabaseService


def identify_plant_task(file_contents: bytes, api_key: str, identification_id: str):
    """
    Background task to process the image and identify the plant.

    Args:
        file_contents (bytes): The uploaded image data.
        api_key (str): The API key to use for Kindwise.
        identification_id (str): The identification ID in the database.
    """
    db_service = DatabaseService()

    try:
        # Process the image
        processed_image = process_image(file_contents)

        # Initialize Kindwise client
        kindwise_client = KindwiseClient(api_key=api_key)

        # Identify the plant
        identification_result = kindwise_client.identify_plant(processed_image)

        # Update the identification record in the database
        db_service.update_identification(identification_id, identification_result)

        print("Plant identification task completed.")
    except Exception as e:
        print(f"Error in plant identification task: {e}")
        # Update the identification record with error status
        db_service.update_identification_error(identification_id, str(e))
