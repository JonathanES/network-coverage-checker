from typing import Annotated, Dict, Any
from pydantic import BaseModel, Field
from src.models import coverage


class NetworkCoverage(BaseModel):
    """API serializer for network coverage information"""

    network_2g: Annotated[
        bool, Field(description="2G network coverage availability", alias="2G")
    ]
    network_3g: Annotated[
        bool, Field(description="3G network coverage availability", alias="3G")
    ]
    network_4g: Annotated[
        bool, Field(description="4G network coverage availability", alias="4G")
    ]

    @classmethod
    def from_model(cls, domain: coverage.NetworkCoverage) -> "NetworkCoverage":
        """Convert domain dataclass to API serializer"""
        return cls(
            **{
                "2G": domain.network_2g,
                "3G": domain.network_3g,
                "4G": domain.network_4g,
            }
        )


class CoverageResponse:
    """Coverage response handler with conversion and type annotation"""

    @staticmethod
    def from_domain(domain_results: Any) -> Dict[str, Dict[str, NetworkCoverage]]:
        """Convert domain models to API serializers"""
        converted = {}
        for location_id, operator_coverage in domain_results.items():
            if isinstance(operator_coverage, dict):
                converted[location_id] = {
                    operator: NetworkCoverage.from_model(network_coverage)
                    for operator, network_coverage in operator_coverage.items()
                }
            else:
                converted[location_id] = operator_coverage
        return converted


CoverageResponseType = Annotated[
    Dict[str, Dict[str, NetworkCoverage]],
    Field(
        description="Network coverage response mapped by location ID",
        examples=[
            {
                "id1": {
                    "orange": {"2G": True, "3G": True, "4G": False},
                    "sfr": {"2G": True, "3G": True, "4G": True},
                    "bouygues": {"2G": True, "3G": True, "4G": False},
                },
                "id4": {
                    "orange": {"2G": True, "3G": True, "4G": False},
                    "bouygues": {"2G": True, "3G": False, "4G": False},
                    "sfr": {"2G": True, "3G": True, "4G": False},
                },
            }
        ],
    ),
]
