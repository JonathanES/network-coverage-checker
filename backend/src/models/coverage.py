from dataclasses import dataclass
from typing import Dict


@dataclass
class NetworkCoverage:
    """Domain model for network coverage by mobile network generation"""

    network_2g: bool
    network_3g: bool
    network_4g: bool


OperatorCoverage = Dict[str, NetworkCoverage]

LocationCoverageResults = Dict[str, OperatorCoverage]
