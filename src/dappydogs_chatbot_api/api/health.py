from typing import Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict

from dappydogs_chatbot_api.settings import Settings

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["alive", "ready"]
    service: str


def _settings_from(request: Request) -> Settings:
    settings: Settings = request.app.state.settings
    return settings


@router.get("/health/live", response_model=HealthResponse)
async def liveness(request: Request) -> HealthResponse:
    settings = _settings_from(request)
    return HealthResponse(status="alive", service=settings.service_name)


@router.get("/health/ready", response_model=HealthResponse)
async def readiness(request: Request) -> HealthResponse:
    """Confirm base configuration loaded; no external dependencies exist yet."""
    settings = _settings_from(request)
    return HealthResponse(status="ready", service=settings.service_name)
