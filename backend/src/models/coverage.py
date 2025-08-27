from dataclasses import dataclass
from typing import Dict


@dataclass
class NetworkCoverage:
    """Domain model for network coverage by mobile network generation"""

    network_2g: bool
    network_3g: bool
    network_4g: bool


# Dynamic operator coverage - maps operator name to their network coverage
OperatorCoverage = Dict[str, NetworkCoverage]

LocationCoverageResults = Dict[str, OperatorCoverage]
