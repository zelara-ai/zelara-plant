from kindwise.plant import PlantApi, PlantIdentification
from src.config import settings


class KindwiseClient:
    def __init__(self, api_key=None):
        """
        Initializes the Kindwise API client.
        """
        self.api = PlantApi(api_key=api_key or settings.kindwise_api_key)

    def identify_plant(self, image_data: bytes):
        """
        Identifies the plant using the Kindwise API.

        Args:
            image_data (bytes): The processed image data.

        Returns:
            dict: The identification result.

        Raises:
            Exception: If identification fails.
        """
        try:
            # Call the identify method of the Kindwise API
            result: PlantIdentification = self.api.identify(
                image=[image_data],
                details=["common_names", "taxonomy", "classification"],
                similar_images=False,
            )
            # Return the result as a dictionary
            return result.dict()
        except Exception as e:
            # Handle exceptions
            print(f"Error identifying plant: {e}")
            raise e
