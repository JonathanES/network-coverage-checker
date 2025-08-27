from fastapi import HTTPException
from src.api.serializers import CoverageRequestBody
from src.api.serializers.coverage.responses import (
    CoverageResponse,
    CoverageResponseType,
)
from src.services.coverage_service import CoverageService
from src.models.coverage import LocationCoverageResults

coverage_service = CoverageService()


async def get_coverage_for_locations(
    request: CoverageRequestBody,
) -> CoverageResponseType:
    """
    Handle HTTP request for network coverage information for multiple locations

    This view is responsible for:
    - HTTP request/response handling
    - Input validation (via Pydantic)
    - Calling business logic service
    - Converting domain models to API serializers
    - Error handling and HTTP status codes
    """
    try:
        domain_results: LocationCoverageResults = (
            await coverage_service.get_coverage_for_locations(request)
        )
        api_results = CoverageResponse.from_domain(domain_results)
        return api_results

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
