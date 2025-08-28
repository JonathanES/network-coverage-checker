import pytest
from unittest.mock import AsyncMock, Mock
from src.services.coverage_service import CoverageService
from src.models.coverage import NetworkCoverage
from src.models.records import CoverageRecord


@pytest.fixture
def mock_coverage_records():
    """Fixture for coverage records test data"""
    return [
        CoverageRecord(
            operator="Orange",
            x=650000,
            y=6860000,
            network_2g=1,
            network_3g=1,
            network_4g=1,
        ),
        CoverageRecord(
            operator="SFR",
            x=650001,
            y=6860001,
            network_2g=1,
            network_3g=0,
            network_4g=1,
        ),
        CoverageRecord(
            operator="Bouygues",
            x=700000,  # Far away location
            y=6900000,
            network_2g=0,
            network_3g=1,
            network_4g=1,
        ),
    ]


@pytest.fixture
def mock_geocoding_service():
    """Fixture for geocoding service mock"""
    mock = AsyncMock()
    mock.geocode_address.return_value = (48.8566, 2.3522)  # Paris coordinates
    return mock


@pytest.fixture
def mock_coordinate_service():
    """Fixture for coordinate service mock"""
    mock = Mock()
    mock.lambert93_to_gps.return_value = (2.3522, 48.8566)  # lon, lat
    mock.calculate_distance.return_value = 5.0  # Within 5km
    return mock


@pytest.fixture
def mock_coverage_loader():
    """Fixture for coverage data loader mock"""
    mock = Mock()
    return mock


@pytest.fixture
def coverage_service_with_mocks(
    monkeypatch,
    mock_coverage_records,
    mock_geocoding_service,
    mock_coordinate_service,
    mock_coverage_loader,
):
    """Fixture for coverage service with all dependencies mocked"""
    # Mock the loader to return our test data
    mock_coverage_loader.load_data.return_value = mock_coverage_records

    # Create service and inject mocks
    service = CoverageService()
    service.loader = mock_coverage_loader
    service.geocoding_service = mock_geocoding_service
    service.coordinate_service = mock_coordinate_service

    return service


class TestCoverageService:
    """Unit tests for CoverageService"""

    def test_coverage_records_property(
        self, coverage_service_with_mocks, mock_coverage_records
    ):
        """Test that coverage_records property returns loader data"""
        records = coverage_service_with_mocks.coverage_records
        assert records == mock_coverage_records
        coverage_service_with_mocks.loader.load_data.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_coverage_for_locations_single_location(
        self, coverage_service_with_mocks
    ):
        """Test getting coverage for a single location"""
        locations = {"loc1": "157 boulevard Mac Donald 75019 Paris"}

        result = await coverage_service_with_mocks.get_coverage_for_locations(locations)

        assert "loc1" in result
        assert isinstance(result["loc1"]["orange"], NetworkCoverage)
        assert result["loc1"]["orange"].network_2g is True
        assert result["loc1"]["orange"].network_3g is True
        assert result["loc1"]["orange"].network_4g is True

    @pytest.mark.asyncio
    async def test_get_coverage_for_locations_multiple_locations(
        self, coverage_service_with_mocks
    ):
        """Test getting coverage for multiple locations"""
        locations = {
            "loc1": "157 boulevard Mac Donald 75019 Paris",
            "loc2": "5 avenue Anatole France 75007 Paris",
        }

        result = await coverage_service_with_mocks.get_coverage_for_locations(locations)

        assert len(result) == 2
        assert "loc1" in result
        assert "loc2" in result

    @pytest.mark.asyncio
    async def test_get_coverage_for_locations_geocoding_failure(
        self, coverage_service_with_mocks
    ):
        """Test handling of geocoding failures"""
        # Mock geocoding to return None (failure)
        coverage_service_with_mocks.geocoding_service.geocode_address.return_value = (
            None
        )

        locations = {"loc1": "invalid address"}
        result = await coverage_service_with_mocks.get_coverage_for_locations(locations)

        # Should handle the failure gracefully and return empty result for that location
        assert len(result) == 0 or result.get("loc1") == {}

    def test_lookup_coverage_by_coordinates_with_coverage(
        self, coverage_service_with_mocks
    ):
        """Test coverage lookup when towers are in range"""
        lat, lon = 48.8566, 2.3522

        result = coverage_service_with_mocks._lookup_coverage_by_coordinates(lat, lon)

        # Should find Orange and SFR (mocked to be within range)
        assert "orange" in result
        assert "sfr" in result
        assert result["orange"]["2G"] is True
        assert result["sfr"]["2G"] is True
        assert result["sfr"]["3G"] is False  # No 3G coverage for SFR

    def test_lookup_coverage_by_coordinates_no_coverage(
        self, coverage_service_with_mocks
    ):
        """Test coverage lookup when no towers are in range"""
        # Mock coordinate service to return large distance
        coverage_service_with_mocks.coordinate_service.calculate_distance.return_value = (
            50.0
        )

        lat, lon = 48.8566, 2.3522
        result = coverage_service_with_mocks._lookup_coverage_by_coordinates(lat, lon)

        # Should return empty dict when no towers in range
        assert result == {}

    def test_build_operator_coverage(self, coverage_service_with_mocks):
        """Test conversion of raw coverage data to NetworkCoverage objects"""
        coverage_data = {
            "orange": {"2G": True, "3G": True, "4G": False},
            "sfr": {"2G": False, "3G": True, "4G": True},
        }

        result = coverage_service_with_mocks._build_operator_coverage(coverage_data)

        assert isinstance(result["orange"], NetworkCoverage)
        assert result["orange"].network_2g is True
        assert result["orange"].network_3g is True
        assert result["orange"].network_4g is False

        assert isinstance(result["sfr"], NetworkCoverage)
        assert result["sfr"].network_2g is False
        assert result["sfr"].network_3g is True
        assert result["sfr"].network_4g is True

    def test_build_operator_coverage_missing_networks(
        self, coverage_service_with_mocks
    ):
        """Test handling of missing network data"""
        coverage_data = {"orange": {"2G": True}}  # Missing 3G and 4G

        result = coverage_service_with_mocks._build_operator_coverage(coverage_data)

        # Should default missing networks to False
        assert result["orange"].network_2g is True
        assert result["orange"].network_3g is False
        assert result["orange"].network_4g is False
