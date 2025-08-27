import httpx
from typing import Optional, Tuple
from pydantic import ValidationError
from src.models.geocoding import GeocodeResponse
import logging

logger = logging.getLogger(__name__)


class GeocodingService:
    """
    Service for geocoding addresses using French government API

    Docs:
      - Overview & reference: https://geoservices.ign.fr/documentation/services/services-geoplateforme/geocodage
    """

    BASE_URL = "https://api-adresse.data.gouv.fr"

    async def geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """
        Geocode a French address to GPS coordinates

        Args:
            address: Address string to geocode

        Returns:
            Tuple of (latitude, longitude) or None if geocoding fails
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/search/", params={"q": address, "limit": 1}
                )
                response.raise_for_status()

                try:
                    geocode_response = GeocodeResponse(**response.json())
                except ValidationError as e:
                    logger.error(f"Invalid geocoding API response for '{address}': {e}")
                    return None

                if not geocode_response.features:
                    logger.warning(f"No geocoding results found for address: {address}")
                    return None

                feature = geocode_response.features[0]
                coordinates = feature.geometry.coordinates

                longitude, latitude = coordinates

                logger.info(f"Geocoded '{address}' to ({latitude}, {longitude})")
                return latitude, longitude

        except httpx.RequestError as e:
            logger.error(f"Network error during geocoding for '{address}': {e}")
            return None
        except (KeyError, IndexError, ValueError) as e:
            logger.error(f"Error parsing geocoding response for '{address}': {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during geocoding for '{address}': {e}")
            return None
