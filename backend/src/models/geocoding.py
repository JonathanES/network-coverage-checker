from typing import List, Optional
from pydantic import BaseModel, Field


class GeocodeGeometry(BaseModel):
    """Geometry data from geocoding API"""

    type: str
    coordinates: List[float] = Field(
        ..., min_items=2, max_items=2, description="[longitude, latitude]"
    )


class GeocodeProperties(BaseModel):
    """Properties data from geocoding API"""

    label: str = None
    score: float = None
    housenumber: str = None
    id: str = None
    name: str = None
    postcode: str = None
    citycode: str = None
    x: float = None
    y: float = None
    city: str = None
    district: str = None
    context: str = None
    type: str = None
    importance: float = None
    street: str = None
    _type: str = None


class GeocodeFeature(BaseModel):
    """Feature from geocoding API response"""

    type: str
    geometry: GeocodeGeometry
    properties: GeocodeProperties


class GeocodeResponse(BaseModel):
    """Response from French government geocoding API"""

    type: str
    features: List[GeocodeFeature]
    query: str
