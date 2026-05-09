"""Integration test for app startup + healthz."""

import pytest
from httpx import ASGITransport, AsyncClient

from customer_inquiry_dashboard.main import create_app


@pytest.mark.asyncio
async def test_app_startup_and_healthz() -> None:
    app = create_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
