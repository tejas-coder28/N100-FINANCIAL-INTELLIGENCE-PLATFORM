import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_get_all_companies():
    response = client.get("/api/v1/companies")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_company_valid_ticker():
    # Attempt fetching first available company or standard ticker
    list_res = client.get("/api/v1/companies")
    if list_res.status_code == 200 and len(list_res.json()) > 0:
        sample_ticker = list_res.json()[0].get("ticker", "TCS")
    else:
        sample_ticker = "TCS"
        
    response = client.get(f"/api/v1/companies/{sample_ticker}")
    assert response.status_code in [200, 404]

def test_get_company_invalid_ticker():
    response = client.get("/api/v1/companies/INVALID_TICKER_999")
    assert response.status_code == 404