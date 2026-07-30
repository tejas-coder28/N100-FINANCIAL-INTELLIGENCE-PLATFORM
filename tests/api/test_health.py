import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_endpoint_status():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "ok"
    assert "db_row_counts" in data

def test_health_endpoint_table_counts():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    counts = response.json().get("db_row_counts", {})
    assert len(counts) >= 1