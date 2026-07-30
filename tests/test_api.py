import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.abspath(os.path.curdir))

from src.api.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "db_row_counts" in data

def test_list_companies():
    response = client.get("/api/v1/companies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_screener():
    response = client.get("/api/v1/screener")
    assert response.status_code in [200, 404, 400]

def test_sectors():
    response = client.get("/api/v1/sectors")
    assert response.status_code in [200, 404]

def test_peers():
    # Passed a sample group name to satisfy the {group_name} path parameter
    response = client.get("/api/v1/peers/IT")
    assert response.status_code in [200, 404]

def test_valuation():
    response = client.get("/api/v1/market-cap/TCS")
    assert response.status_code in [200, 404]

def test_portfolio_stats():
    response = client.get("/api/v1/portfolio/stats")
    assert response.status_code in [200, 404]

def test_documents():
    response = client.get("/api/v1/companies/TCS/documents")
    assert response.status_code in [200, 404]
