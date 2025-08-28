import pytest
from unittest.mock import AsyncMock, Mock, patch
import httpx
from pydantic import ValidationError
from src.services.geocoding_service import GeocodingService


@pytest.fixture
def geocoding_service():
    """Fixture for geocoding service instance"""
    return GeocodingService()


@pytest.fixture
def mock_successful_response():
    """Fixture for successful geocoding API response"""
    return {
        "type": "FeatureCollection",
        "query": "157 boulevard Mac Donald 75019 Paris",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [2.3522, 48.8566],  # [longitude, latitude]
                },
                "properties": {
                    "label": "157 Boulevard MacDonald 75019 Paris",
                    "score": 0.8,
                },
            }
        ],
    }


@pytest.fixture
def mock_empty_response():
    """Fixture for empty geocoding API response"""
    return {"type": "FeatureCollection", "query": "nonexistent address", "features": []}


@pytest.fixture
def mock_invalid_response():
    """Fixture for invalid geocoding API response"""
    return {"invalid": "response"}


class TestGeocodingService:
    """Unit tests for GeocodingService"""

    @pytest.mark.asyncio
    async def test_geocode_address_success(
        self, geocoding_service, mock_successful_response
    ):
        """Test successful geocoding of an address"""
        with patch("httpx.AsyncClient") as mock_client:
            # Setup mock response
            mock_response = Mock()
            mock_response.json.return_value = mock_successful_response
            mock_response.raise_for_status.return_value = None

            # Setup mock client
            mock_context_manager = AsyncMock()
            mock_context_manager.__aenter__.return_value.get.return_value = (
                mock_response
            )
            mock_client.return_value = mock_context_manager

            # Test the geocoding
            address = "157 boulevard Mac Donald 75019 Paris"
            result = await geocoding_service.geocode_address(address)

            # Verify result
            assert result is not None
            assert result == (48.8566, 2.3522)  # (latitude, longitude)

            # Verify API was called correctly
            mock_context_manager.__aenter__.return_value.get.assert_called_once_with(
                f"{geocoding_service.BASE_URL}/search/",
                params={"q": address, "limit": 1},
            )

    @pytest.mark.asyncio
    async def test_geocode_address_no_results(
        self, geocoding_service, mock_empty_response
    ):
        """Test geocoding when no results are found"""
        with patch("httpx.AsyncClient") as mock_client:
            # Setup mock response with no features
            mock_response = Mock()
            mock_response.json.return_value = mock_empty_response
            mock_response.raise_for_status.return_value = None

            mock_context_manager = AsyncMock()
            mock_context_manager.__aenter__.return_value.get.return_value = (
                mock_response
            )
            mock_client.return_value = mock_context_manager

            # Test the geocoding
            result = await geocoding_service.geocode_address("nonexistent address")

            # Should return None for no results
            assert result is None

    @pytest.mark.asyncio
    async def test_geocode_address_invalid_response(
        self, geocoding_service, mock_invalid_response
    ):
        """Test geocoding with invalid API response"""
        with patch("httpx.AsyncClient") as mock_client:
            # Setup mock response with invalid structure
            mock_response = Mock()
            mock_response.json.return_value = mock_invalid_response
            mock_response.raise_for_status.return_value = None

            mock_context_manager = AsyncMock()
            mock_context_manager.__aenter__.return_value.get.return_value = (
                mock_response
            )
            mock_client.return_value = mock_context_manager

            # Test the geocoding
            result = await geocoding_service.geocode_address("some address")

            # Should return None for invalid response
            assert result is None

    @pytest.mark.asyncio
    async def test_geocode_address_network_error(self, geocoding_service):
        """Test geocoding with network error"""
        with patch("httpx.AsyncClient") as mock_client:
            # Setup mock to raise network error
            mock_context_manager = AsyncMock()
            mock_context_manager.__aenter__.return_value.get.side_effect = (
                httpx.RequestError("Network error")
            )
            mock_client.return_value = mock_context_manager

            # Test the geocoding
            result = await geocoding_service.geocode_address("some address")

            # Should return None for network error
            assert result is None

    @pytest.mark.asyncio
    async def test_geocode_address_http_error(self, geocoding_service):
        """Test geocoding with HTTP error (4xx/5xx)"""
        with patch("httpx.AsyncClient") as mock_client:
            # Setup mock response to raise HTTP error
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "400 Bad Request", request=Mock(), response=Mock()
            )

            mock_context_manager = AsyncMock()
            mock_context_manager.__aenter__.return_value.get.return_value = (
                mock_response
            )
            mock_client.return_value = mock_context_manager

            # Test the geocoding
            result = await geocoding_service.geocode_address("invalid address")

            # Should return None for HTTP error
            assert result is None

    @pytest.mark.asyncio
    async def test_geocode_address_validation_error(self, geocoding_service):
        """Test geocoding with pydantic validation error"""
        with patch("httpx.AsyncClient") as mock_client:
            # Setup mock response with structure that fails validation
            mock_response = Mock()
            mock_response.json.return_value = {"features": ["invalid_feature"]}
            mock_response.raise_for_status.return_value = None

            mock_context_manager = AsyncMock()
            mock_context_manager.__aenter__.return_value.get.return_value = (
                mock_response
            )
            mock_client.return_value = mock_context_manager

            # Test the geocoding
            result = await geocoding_service.geocode_address("some address")

            # Should return None for validation error
            assert result is None

    @pytest.mark.asyncio
    async def test_geocode_address_unexpected_error(self, geocoding_service):
        """Test geocoding with unexpected error"""
        with patch("httpx.AsyncClient") as mock_client:
            # Setup mock to raise unexpected error
            mock_context_manager = AsyncMock()
            mock_context_manager.__aenter__.return_value.get.side_effect = Exception(
                "Unexpected error"
            )
            mock_client.return_value = mock_context_manager

            # Test the geocoding
            result = await geocoding_service.geocode_address("some address")

            # Should return None for unexpected error
            assert result is None

    @pytest.mark.asyncio
    async def test_geocode_address_empty_string(
        self, geocoding_service, mock_empty_response
    ):
        """Test geocoding with empty address string"""
        with patch("httpx.AsyncClient") as mock_client:
            # Setup mock response for empty address
            mock_response = Mock()
            mock_response.json.return_value = mock_empty_response
            mock_response.raise_for_status.return_value = None

            mock_context_manager = AsyncMock()
            mock_context_manager.__aenter__.return_value.get.return_value = (
                mock_response
            )
            mock_client.return_value = mock_context_manager

            # Test with empty address
            result = await geocoding_service.geocode_address("")

            # Should return None for empty address
            assert result is None
