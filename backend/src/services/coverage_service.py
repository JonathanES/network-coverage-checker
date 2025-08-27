from typing import Dict, List
from src.data.coverage_loader import CoverageDataLoader
from src.models.coverage import (
    NetworkCoverage,
    OperatorCoverage,
    LocationCoverageResults,
)
from src.models.records import CoverageRecord
from src.services.geocoding_service import GeocodingService
from src.services.coordinate_service import CoordinateService

NETWORK_GEN_RADIUS_KM = {"2G": 30.0, "3G": 5.0, "4G": 10.0}


class CoverageService:
    """Business logic service for network coverage operations"""

    def __init__(self):
        self.loader = CoverageDataLoader(
            "src/data/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93_ver2.csv"
        )
        self.geocoding_service = GeocodingService()
        self.coordinate_service = CoordinateService()

    @property
    def coverage_records(self) -> List[CoverageRecord]:
        """Lazy-loaded coverage records from CSV file"""
        return self.loader.load_data()

    async def get_coverage_for_locations(
        self, locations: Dict[str, str]
    ) -> LocationCoverageResults:
        """
        Get coverage information for multiple locations

        Args:
            locations: Dictionary mapping location IDs to addresses

        Returns:
            Dictionary mapping location IDs to coverage information
        """
        results = {}

        for location_id, address in locations.items():
            coverage_data = await self._process_location_coverage(address)
            results[location_id] = self._build_operator_coverage(coverage_data)

        return results

    async def _process_location_coverage(
        self, address: str
    ) -> Dict[str, Dict[str, bool]]:
        """
        Process coverage for a single location

        Args:
            address: Address string to get coverage for

        Returns:
            Dictionary with operator coverage data
        """
        coordinates = await self.geocoding_service.geocode_address(address)

        if not coordinates:
            return {}

        lat, lon = coordinates
        return self._lookup_coverage_by_coordinates(lat, lon)

    def _lookup_coverage_by_coordinates(
        self, lat: float, lon: float
    ) -> Dict[str, Dict[str, bool]]:
        """
        Aggregate coverage by checking each record once and determining what networks are available
        based on distance.

        For each operator and mobile network generation combination, returns:
        - True: if there's at least one tower of that operator with that network generation within range
        - False: if no towers of that operator with that network generation are found within range
        """
        coverage = {}

        for record in self.coverage_records:
            tower_lon, tower_lat = self.coordinate_service.lambert93_to_gps(
                record.x, record.y
            )

            distance = self.coordinate_service.calculate_distance(
                lat, lon, tower_lat, tower_lon
            )

            operator = record.operator.lower()

            if operator not in coverage:
                coverage[operator] = {"2G": False, "3G": False, "4G": False}

            if record.network_2g == 1 and distance <= NETWORK_GEN_RADIUS_KM["2G"]:
                coverage[operator]["2G"] = True

            if record.network_3g == 1 and distance <= NETWORK_GEN_RADIUS_KM["3G"]:
                coverage[operator]["3G"] = True

            if record.network_4g == 1 and distance <= NETWORK_GEN_RADIUS_KM["4G"]:
                coverage[operator]["4G"] = True

        return coverage

    def _build_operator_coverage(
        self, coverage_data: Dict[str, Dict[str, bool]]
    ) -> OperatorCoverage:
        """
        Convert raw coverage data to OperatorCoverage model

        Args:
            coverage_data: Raw coverage data by operator

        Returns:
            OperatorCoverage instance (Dict[str, NetworkCoverage])
        """
        result = {}
        for operator, networks in coverage_data.items():
            result[operator] = NetworkCoverage(
                network_2g=networks.get("2G", False),
                network_3g=networks.get("3G", False),
                network_4g=networks.get("4G", False),
            )
        return result
