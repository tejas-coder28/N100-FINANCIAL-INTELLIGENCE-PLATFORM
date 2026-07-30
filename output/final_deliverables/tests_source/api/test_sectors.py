import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_get_all_sectors():
    response = client.get("/api/v1/sectors")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_sector_companies():
    response = client.get("/api/v1/sectors/IT/companies")
    assert response.status_code in [200, 404]

def test_get_invalid_sector():
    response = client.get("/api/v1/sectors/NON_EXISTENT_SECTOR/companies")
    assert response.status_code == 404