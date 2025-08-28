from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class NetworkCoverage:
    """Domain model for network coverage by mobile network generation"""

    network_2g: bool
    network_3g: bool
    network_4g: bool


@dataclass
class LocationCoverageData:
    """Coverage data for a single location, with optional error handling"""

    error: Optional[str]
    operators: Dict[str, NetworkCoverage]


OperatorCoverage = Dict[str, NetworkCoverage]

LocationCoverageResults = Dict[str, LocationCoverageData]
