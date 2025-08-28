import pytest
import math
from unittest.mock import patch, Mock
from src.services.coordinate_service import CoordinateService, EARTH_RADIUS_KM


@pytest.fixture
def coordinate_service():
    """Fixture for coordinate service instance"""
    return CoordinateService()


@pytest.fixture
def paris_lambert93():
    """Fixture for Paris coordinates in Lambert93"""
    return (652376, 6862327)


@pytest.fixture
def paris_gps():
    """Fixture for Paris coordinates in GPS (WGS84)"""
    return (2.3488, 48.8534)


@pytest.fixture
def lyon_gps():
    """Fixture for Lyon coordinates in GPS (WGS84)"""
    return (4.8357, 45.7640)


class TestCoordinateService:
    """Unit tests for CoordinateService"""

    def test_lambert93_to_gps_conversion(self, coordinate_service, paris_lambert93):
        """Test conversion from Lambert93 to GPS coordinates"""
        x, y = paris_lambert93

        lon, lat = coordinate_service.lambert93_to_gps(x, y)

        # Verify coordinates are in reasonable range for France
        assert 41.0 < lat < 51.5  # France latitude range
        assert -5.0 < lon < 10.0  # France longitude range

        # Should return longitude, latitude tuple
        assert isinstance(lon, float)
        assert isinstance(lat, float)

    def test_lambert93_to_gps_caching(self, coordinate_service, paris_lambert93):
        """Test that Lambert93 to GPS conversion results are cached"""
        x, y = paris_lambert93

        # First call
        result1 = coordinate_service.lambert93_to_gps(x, y)

        # Second call should use cache
        result2 = coordinate_service.lambert93_to_gps(x, y)

        # Results should be identical (same object from cache)
        assert result1 == result2
        assert result1 is result2  # Same object reference

    def test_lambert93_to_gps_different_coordinates(self, coordinate_service):
        """Test conversion with different coordinates"""
        # Test with different coordinates
        coords1 = coordinate_service.lambert93_to_gps(650000, 6860000)
        coords2 = coordinate_service.lambert93_to_gps(700000, 6900000)

        # Should return different results
        assert coords1 != coords2

    def test_calculate_distance_same_point(self, coordinate_service, paris_gps):
        """Test distance calculation between same point"""
        lon, lat = paris_gps

        distance = coordinate_service.calculate_distance(lat, lon, lat, lon)

        # Distance should be 0 for same point
        assert distance == 0.0

    def test_calculate_distance_known_cities(
        self, coordinate_service, paris_gps, lyon_gps
    ):
        """Test distance calculation between known cities"""
        paris_lon, paris_lat = paris_gps
        lyon_lon, lyon_lat = lyon_gps

        distance = coordinate_service.calculate_distance(
            paris_lat, paris_lon, lyon_lat, lyon_lon
        )

        # Paris to Lyon is approximately 390-410 km
        assert 380 < distance < 420
        assert isinstance(distance, float)

    def test_calculate_distance_symmetry(self, coordinate_service, paris_gps, lyon_gps):
        """Test that distance calculation is symmetric"""
        paris_lon, paris_lat = paris_gps
        lyon_lon, lyon_lat = lyon_gps

        distance1 = coordinate_service.calculate_distance(
            paris_lat, paris_lon, lyon_lat, lyon_lon
        )
        distance2 = coordinate_service.calculate_distance(
            lyon_lat, lyon_lon, paris_lat, paris_lon
        )

        # Distance should be the same regardless of order
        assert abs(distance1 - distance2) < 0.001  # Allow for floating point precision

    def test_calculate_distance_short_distance(self, coordinate_service):
        """Test distance calculation for short distances"""
        # Two points very close to each other in Paris
        lat1, lon1 = 48.8566, 2.3522  # Notre-Dame
        lat2, lon2 = 48.8606, 2.3376  # Louvre

        distance = coordinate_service.calculate_distance(lat1, lon1, lat2, lon2)

        # Distance should be approximately 1.5-2.0 km
        assert 1.0 < distance < 3.0

    def test_calculate_distance_long_distance(self, coordinate_service):
        """Test distance calculation for long distances"""
        # Paris to New York (approximate)
        paris_lat, paris_lon = 48.8566, 2.3522
        ny_lat, ny_lon = 40.7589, -73.9851

        distance = coordinate_service.calculate_distance(
            paris_lat, paris_lon, ny_lat, ny_lon
        )

        # Paris to New York is approximately 5800-5900 km
        assert 5700 < distance < 6000

    def test_calculate_distance_equator_poles(self, coordinate_service):
        """Test distance calculation from equator to pole"""
        # From equator to north pole
        equator_lat, equator_lon = 0.0, 0.0
        pole_lat, pole_lon = 90.0, 0.0

        distance = coordinate_service.calculate_distance(
            equator_lat, equator_lon, pole_lat, pole_lon
        )

        # Quarter of Earth's circumference ≈ 10,000 km
        expected_distance = math.pi * EARTH_RADIUS_KM / 2
        assert abs(distance - expected_distance) < 10  # Allow small error

    def test_calculate_distance_negative_coordinates(self, coordinate_service):
        """Test distance calculation with negative coordinates"""
        # Southern hemisphere coordinates
        lat1, lon1 = -33.8688, 151.2093  # Sydney
        lat2, lon2 = -37.8136, 144.9631  # Melbourne

        distance = coordinate_service.calculate_distance(lat1, lon1, lat2, lon2)

        # Sydney to Melbourne is approximately 700-800 km
        assert 650 < distance < 850

    def test_earth_radius_constant(self):
        """Test that Earth radius constant is reasonable"""
        # Earth radius should be around 6371 km
        assert 6350 < EARTH_RADIUS_KM < 6400

    @patch("pyproj.transform")
    def test_lambert93_to_gps_with_mock(self, mock_transform, coordinate_service):
        """Test Lambert93 to GPS conversion with mocked pyproj"""
        # Mock the transform function
        mock_transform.return_value = (2.3488, 48.8534)

        x, y = 652376, 6862327
        result = coordinate_service.lambert93_to_gps(x, y)

        # Verify the mock was called
        mock_transform.assert_called_once()

        # Verify result
        assert result == (2.3488, 48.8534)

    def test_cache_key_format(self, coordinate_service):
        """Test that cache keys are formatted correctly"""
        x, y = 650000.0, 6860000.0

        # Call the method to populate cache
        coordinate_service.lambert93_to_gps(x, y)

        # Check that cache key exists
        expected_key = f"{x},{y}"
        assert expected_key in coordinate_service._gps_cache

    def test_cache_persistence(self, coordinate_service):
        """Test that cache persists across multiple calls"""
        coordinates = [(650000, 6860000), (700000, 6900000), (750000, 6950000)]

        # Make multiple calls
        results = []
        for x, y in coordinates:
            result = coordinate_service.lambert93_to_gps(x, y)
            results.append(result)

        # Verify cache has all entries
        assert len(coordinate_service._gps_cache) == len(coordinates)

        # Make same calls again and verify results are identical
        for i, (x, y) in enumerate(coordinates):
            cached_result = coordinate_service.lambert93_to_gps(x, y)
            assert cached_result == results[i]
