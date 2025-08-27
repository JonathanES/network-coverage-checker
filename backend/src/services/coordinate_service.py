import math
import pyproj
from typing import Dict, List, Tuple
from src.models.records import CoverageRecord

# Earth radius in kilometers
EARTH_RADIUS_KM = 6371.0


class CoordinateService:
    """Service for coordinate conversion and distance calculations"""

    def __init__(self):
        self._lambert_proj = pyproj.Proj(
            "+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 "
            "+y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        )
        self._wgs84_proj = pyproj.Proj(
            "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
        )
        self._gps_cache: Dict[str, Tuple[float, float]] = {}

    def lambert93_to_gps(self, x: float, y: float) -> Tuple[float, float]:
        """
        Convert Lambert93 coordinates to GPS (WGS84) coordinates

        Args:
            x: Lambert93 X coordinate
            y: Lambert93 Y coordinate

        Returns:
            Tuple of (longitude, latitude) in WGS84
        """
        # Use cache to avoid repeated conversions
        cache_key = f"{x},{y}"

        if cache_key not in self._gps_cache:
            longitude, latitude = pyproj.transform(
                self._lambert_proj, self._wgs84_proj, x, y
            )
            self._gps_cache[cache_key] = (longitude, latitude)

        return self._gps_cache[cache_key]

    def calculate_distance(
        self, lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        """
        Calculate the great circle distance between two points using the Haversine formula

        Reference: https://en.wikipedia.org/wiki/Haversine_formula

        Args:
            lat1, lon1: First point coordinates (latitude, longitude)
            lat2, lon2: Second point coordinates (latitude, longitude)

        Returns:
            Distance in kilometers
        """
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.asin(math.sqrt(a))

        return EARTH_RADIUS_KM * c
