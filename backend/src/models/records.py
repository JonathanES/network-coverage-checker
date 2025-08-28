from typing import Annotated
from pydantic import BaseModel, Field


class CoverageRecord(BaseModel):
    """Data model for a single coverage record from the CSV file"""

    operator: Annotated[str, Field(description="Network operator name")]
    x: Annotated[int, Field(description="Lambert93 X coordinate")]
    y: Annotated[int, Field(description="Lambert93 Y coordinate")]
    network_2g: Annotated[int, Field(description="2G coverage (0 or 1)")]
    network_3g: Annotated[int, Field(description="3G coverage (0 or 1)")]
    network_4g: Annotated[int, Field(description="4G coverage (0 or 1)")]
