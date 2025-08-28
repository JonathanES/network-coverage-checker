from fastapi import APIRouter
from src.api import views

router = APIRouter(prefix="/api/v1")

router.add_api_route(
    "/coverage",
    views.get_coverage_for_locations,
    methods=["POST"],
    summary="Get network coverage for multiple locations",
    description="Returns network coverage information for the provided locations",
)
