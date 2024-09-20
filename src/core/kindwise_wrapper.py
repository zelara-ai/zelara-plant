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
            dict: The simplified identification result.

        Raises:
            Exception: If identification fails.
        """
        try:
            # Call the identify method of the Kindwise API
            result: PlantIdentification = self.api.identify(
                image=[image_data],
                details=["common_names", "taxonomy", "classification"],
            )

            # Extract relevant data
            simplified_result = self._simplify_result(result)
            return simplified_result

        except Exception as e:
            # Handle exceptions
            print(f"Error identifying plant: {e}")
            raise e

    def _simplify_result(self, result: PlantIdentification) -> dict:
        """
        Simplifies the Kindwise API result to include only relevant data.

        Args:
            result (PlantIdentification): The original API result.

        Returns:
            dict: The simplified result.
        """
        suggestions = []
        for suggestion in result.result.classification.suggestions:
            suggestions.append({
                "id": suggestion.id,
                "name": suggestion.name,
                "probability": suggestion.probability,
                "common_names": suggestion.details.get('common_names', []),
                "taxonomy": suggestion.details.get('taxonomy', {}),
            })

        simplified_result = {
            "plant_name": suggestions[0]["name"] if suggestions else None,
            "common_names": suggestions[0]["common_names"] if suggestions else [],
            "probability": suggestions[0]["probability"] if suggestions else None,
            "taxonomy": suggestions[0]["taxonomy"] if suggestions else {},
            "identification_id": result.access_token,
            "is_plant": result.result.is_plant.binary,
            "created": result.created.isoformat(),
        }

        return simplified_result
