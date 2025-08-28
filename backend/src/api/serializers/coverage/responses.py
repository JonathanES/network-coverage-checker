from typing import Annotated, Dict, Any, Optional
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


class LocationCoverageResponse(BaseModel):
    """API serializer for location coverage data with error handling"""

    error: Optional[str] = Field(
        description="Error message if location processing failed"
    )
    operators: Dict[str, NetworkCoverage] = Field(
        description="Coverage data by operator"
    )


class CoverageResponse:
    """Coverage response handler with conversion and type annotation"""

    @staticmethod
    def from_domain(domain_results: Any) -> Dict[str, LocationCoverageResponse]:
        """Convert domain models to API serializers"""
        converted = {}
        for location_id, location_data in domain_results.items():
            # Handle LocationCoverageData objects
            if hasattr(location_data, "error") and hasattr(location_data, "operators"):
                operators_converted = {}
                for operator, network_coverage in location_data.operators.items():
                    operators_converted[operator] = NetworkCoverage.from_model(
                        network_coverage
                    )

                converted[location_id] = LocationCoverageResponse(
                    error=location_data.error, operators=operators_converted
                )
            else:
                converted[location_id] = LocationCoverageResponse(
                    error=None, operators=location_data
                )
        return converted


CoverageResponseType = Annotated[
    Dict[str, LocationCoverageResponse],
    Field(
        description="Network coverage response mapped by location ID with error handling",
        examples=[
            {
                "id1": {
                    "error": None,
                    "operators": {
                        "orange": {"2G": True, "3G": True, "4G": False},
                        "sfr": {"2G": True, "3G": True, "4G": True},
                        "bouygues": {"2G": True, "3G": True, "4G": False},
                    },
                },
                "id4": {
                    "error": "Could not geocode address: invalid address",
                    "operators": {},
                },
            }
        ],
    ),
]
