import pytest
from unittest.mock import AsyncMock
from src.models.coverage import NetworkCoverage


@pytest.fixture
def mock_coverage_service(monkeypatch):
    """Fixture to mock the coverage service"""
    mock_service = AsyncMock()
    monkeypatch.setattr("src.api.views.coverage_service", mock_service)
    return mock_service


@pytest.fixture
def single_location_coverage_data():
    """Fixture for single location coverage test data"""
    return {
        "location1": {
            "orange": NetworkCoverage(
                network_2g=True, network_3g=True, network_4g=True
            ),
            "sfr": NetworkCoverage(network_2g=True, network_3g=False, network_4g=True),
            "bouygues": NetworkCoverage(
                network_2g=False, network_3g=True, network_4g=True
            ),
        }
    }


@pytest.fixture
def multiple_locations_coverage_data():
    """Fixture for multiple locations coverage test data"""
    return {
        "location1": {
            "orange": NetworkCoverage(
                network_2g=True, network_3g=True, network_4g=True
            ),
            "sfr": NetworkCoverage(network_2g=True, network_3g=False, network_4g=True),
        },
        "location2": {
            "orange": NetworkCoverage(
                network_2g=False, network_3g=True, network_4g=True
            ),
            "bouygues": NetworkCoverage(
                network_2g=True, network_3g=True, network_4g=False
            ),
        },
    }


class TestAPIIntegration:
    """Integration tests for the API endpoints"""

    def test_health_endpoint(self, client):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data == {"status": "ok"}

    def test_coverage_endpoint_success(
        self, mock_coverage_service, single_location_coverage_data, client
    ):
        """Test successful coverage request with mocked service"""
        mock_coverage_service.get_coverage_for_locations.return_value = (
            single_location_coverage_data
        )

        payload = {"location1": "157 boulevard Mac Donald 75019 Paris"}
        response = client.post("/api/v1/coverage", json=payload)

        assert response.status_code == 200
        data = response.json()

        assert "location1" in data
        location_data = data["location1"]

        assert "orange" in location_data
        assert "sfr" in location_data
        assert "bouygues" in location_data

        for operator in ["orange", "sfr", "bouygues"]:
            coverage = location_data[operator]
            assert "2G" in coverage
            assert "3G" in coverage
            assert "4G" in coverage
            assert isinstance(coverage["2G"], bool)
            assert isinstance(coverage["3G"], bool)
            assert isinstance(coverage["4G"], bool)

    def test_coverage_endpoint_multiple_locations(
        self, mock_coverage_service, multiple_locations_coverage_data, client
    ):
        """Test coverage request with multiple locations"""
        mock_coverage_service.get_coverage_for_locations.return_value = (
            multiple_locations_coverage_data
        )

        payload = {
            "location1": "157 boulevard Mac Donald 75019 Paris",
            "location2": "5 avenue Anatole France 75007 Paris",
        }
        response = client.post("/api/v1/coverage", json=payload)

        assert response.status_code == 200
        data = response.json()

        assert len(data) == 2
        assert "location1" in data
        assert "location2" in data

    def test_coverage_endpoint_empty_locations(self, client):
        """Test coverage request with empty locations"""
        payload = {}
        response = client.post("/api/v1/coverage", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data == {}

    def test_coverage_endpoint_invalid_payload(self, client):
        """Test coverage request with invalid payload"""
        invalid_payloads = [
            {"location1": 123},  # Wrong type - should be string
            {"location1": None},  # None value
        ]

        for payload in invalid_payloads:
            response = client.post("/api/v1/coverage", json=payload)
            assert response.status_code == 422

    def test_coverage_endpoint_service_error(self, mock_coverage_service, client):
        """Test coverage request when service raises an error"""
        mock_coverage_service.get_coverage_for_locations.side_effect = ValueError(
            "Invalid address"
        )

        payload = {"location1": "invalid address"}
        response = client.post("/api/v1/coverage", json=payload)

        assert response.status_code == 400
        data = response.json()
        assert "Invalid request" in data["detail"]

    def test_coverage_endpoint_internal_error(self, mock_coverage_service, client):
        """Test coverage request when service raises an unexpected error"""
        mock_coverage_service.get_coverage_for_locations.side_effect = Exception(
            "Database connection failed"
        )

        payload = {"location1": "157 boulevard Mac Donald 75019 Paris"}
        response = client.post("/api/v1/coverage", json=payload)

        assert response.status_code == 500
        data = response.json()
        assert data["detail"] == "Internal server error"

    def test_coverage_endpoint_malformed_json(self, client):
        """Test coverage request with malformed JSON"""
        response = client.post(
            "/api/v1/coverage",
            content="invalid json",
            headers={"content-type": "application/json"},
        )
        assert response.status_code == 422
