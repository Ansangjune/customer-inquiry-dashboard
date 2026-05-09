"""Shared test fixtures."""

import pytest
from fastapi.testclient import TestClient

from customer_inquiry_dashboard.main import create_app


@pytest.fixture
def client() -> TestClient:
    app = create_app()
    return TestClient(app)
