import pytest
from unittest.mock import patch, AsyncMock

from fastapi.testclient import TestClient
from backend.main import app
from backend.services.data_analyzer import process_census_data, process_coingecko_data

client = TestClient(app)

def test_process_census_data_valid():
    raw_data = {
        "data": [
            {"Year": 2021, "Population": 100},
            {"Year": 2022, "Population": 110}
        ]
    }
    result = process_census_data(raw_data)
    
    assert "labels" in result
    assert result["labels"] == ["2021", "2022"]
    
    assert "datasets" in result
    assert result["datasets"]["population"] == [100, 110]
    assert result["datasets"]["growth"] == [0.0, 10.0]
    
def test_process_census_data_invalid():
    assert "error" in process_census_data({})

def test_process_coingecko_data_valid():
    raw_data = {
        "data": {
            "active_cryptocurrencies": 1000,
            "markets": 500,
            "total_market_cap": {"usd": 2000000},
            "total_volume": {"usd": 50000},
            "market_cap_percentage": {"btc": 50.5}
        }
    }
    result = process_coingecko_data(raw_data)
    assert "metrics" in result
    assert result["metrics"]["active_cryptocurrencies"] == 1000
    assert result["metrics"]["btc_dominance_pct"] == 50.5


# --- HTTP-level endpoint tests (US3) ---

@patch("backend.main.fetch_datausa_population", new_callable=AsyncMock)
def test_census_endpoint(mock_fetch):
    mock_fetch.return_value = {
        "data": [
            {"Year": "2021", "Population": 331893745},
            {"Year": "2022", "Population": 333287557}
        ]
    }
    response = client.get("/api/census/demographics")
    assert response.status_code == 200
    body = response.json()
    assert "labels" in body
    assert isinstance(body["labels"], list)
    assert all(isinstance(l, str) for l in body["labels"])
    assert "datasets" in body
    assert "population" in body["datasets"]
    assert "growth" in body["datasets"]
    assert "growth_pct" in body["datasets"]
    assert all(isinstance(v, (int, float)) for v in body["datasets"]["population"])


@patch("backend.main.fetch_coingecko_global", new_callable=AsyncMock)
def test_crypto_endpoint(mock_fetch):
    mock_fetch.return_value = {
        "data": {
            "active_cryptocurrencies": 14500,
            "markets": 1200,
            "total_market_cap": {"usd": 2450000000000},
            "total_volume": {"usd": 125000000000},
            "market_cap_percentage": {"btc": 52.5, "eth": 16.2}
        }
    }
    response = client.get("/api/finance/crypto")
    assert response.status_code == 200
    body = response.json()
    assert "metrics" in body
    metrics = body["metrics"]
    assert "active_cryptocurrencies" in metrics
    assert "total_markets" in metrics
    assert "total_market_cap_usd" in metrics
    assert "total_volume_usd" in metrics
    assert "btc_dominance_pct" in metrics


@patch("backend.main.fetch_apis_guru_metrics", new_callable=AsyncMock)
def test_api_demand_endpoint(mock_fetch):
    mock_fetch.return_value = {
        "numAPIs": 2500,
        "numEndpoints": 100000,
        "datasets": [
            {
                "title": "providerCount",
                "data": {
                    "googleapis.com": 350,
                    "azure.com": 200,
                    "amazonaws.com": 180,
                }
            }
        ]
    }
    response = client.get("/api/metrics/api-demand")
    assert response.status_code == 200
    body = response.json()
    assert "metrics" in body
    assert "total_apis" in body["metrics"]
    assert "total_endpoints" in body["metrics"]
    assert "chart_data" in body
    assert "labels" in body["chart_data"]
    assert "counts" in body["chart_data"]
    assert isinstance(body["chart_data"]["labels"], list)
    assert isinstance(body["chart_data"]["counts"], list)
