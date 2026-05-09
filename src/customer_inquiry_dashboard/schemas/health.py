"""Health endpoint response schema."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(description="Service status, typically 'ok'")
    service: str = Field(description="Service identifier")
    version: str = Field(description="Service version")
