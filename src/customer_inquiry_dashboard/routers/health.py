"""/healthz endpoint."""

from fastapi import APIRouter

from customer_inquiry_dashboard.deps import SettingsDep
from customer_inquiry_dashboard.schemas.health import HealthResponse

router = APIRouter()


@router.get("/healthz", response_model=HealthResponse)
async def healthz(settings: SettingsDep) -> HealthResponse:
    return HealthResponse(status="ok", service=settings.service_name, version="0.1.0")
