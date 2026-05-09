"""Unit tests for /api/inquiries/summary."""

from fastapi.testclient import TestClient


def test_summary_returns_200(client: TestClient) -> None:
    resp = client.get("/api/inquiries/summary")
    assert resp.status_code == 200


def test_summary_payload_shape(client: TestClient) -> None:
    body = client.get("/api/inquiries/summary").json()

    assert isinstance(body["total"], int)
    assert body["total"] >= 0
    assert isinstance(body["today"], int)
    assert isinstance(body["last_7_days"], int)

    status = body["by_status"]
    assert set(status.keys()) == {"open", "in_progress", "resolved", "closed"}
    for value in status.values():
        assert isinstance(value, int)
        assert value >= 0

    assert isinstance(body["by_category"], list)
    assert len(body["by_category"]) > 0
    for entry in body["by_category"]:
        assert {"category", "count"} <= entry.keys()
        assert isinstance(entry["category"], str)
        assert isinstance(entry["count"], int)
        assert entry["count"] >= 0

    assert isinstance(body["recent"], list)
    assert len(body["recent"]) > 0
    for inquiry in body["recent"]:
        assert {"id", "customer", "subject", "status", "category", "created_at"} <= inquiry.keys()


def test_summary_status_totals_are_consistent(client: TestClient) -> None:
    body = client.get("/api/inquiries/summary").json()
    status_sum = sum(body["by_status"].values())
    category_sum = sum(entry["count"] for entry in body["by_category"])
    assert status_sum == body["total"]
    assert category_sum == body["total"]
