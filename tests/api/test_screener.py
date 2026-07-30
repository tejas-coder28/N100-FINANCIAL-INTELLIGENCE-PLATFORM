import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_screener_valid_filter():
    response = client.get("/api/v1/screener?min_roe=15")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for company in data:
        if "roe_pct" in company and company["roe_pct"] is not None:
            assert company["roe_pct"] >= 15.0

def test_screener_invalid_param():
    response = client.get("/api/v1/screener?min_roe=invalid_string")
    assert response.status_code == 422 or response.status_code == 400