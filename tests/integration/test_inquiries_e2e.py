"""Integration test for the inquiries summary endpoint."""

from fastapi.testclient import TestClient

from customer_inquiry_dashboard.main import create_app


def test_summary_e2e_via_test_client() -> None:
    app = create_app()
    with TestClient(app) as client:
        resp = client.get("/api/inquiries/summary")
    assert resp.status_code == 200
    body = resp.json()
    assert body["total"] >= 0
    assert "by_status" in body
    assert "recent" in body
