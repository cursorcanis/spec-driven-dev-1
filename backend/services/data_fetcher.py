import httpx
import asyncio
from typing import Dict, Any

async def fetch_datausa_population() -> Dict[str, Any]:
    """Fetches population data from the free Data USA API or uses a fallback if blocked."""
    url = "https://datausa.io/api/data?drilldowns=Nation&measures=Population"
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            # Fallback mock data if the API returns 404 or blocks us
            return {
                "data": [
                    {"ID Nation": "01000US", "Nation": "United States", "ID Year": 2018, "Year": "2018", "Population": 327167434, "Slug Nation": "united-states"},
                    {"ID Nation": "01000US", "Nation": "United States", "ID Year": 2019, "Year": "2019", "Population": 328239523, "Slug Nation": "united-states"},
                    {"ID Nation": "01000US", "Nation": "United States", "ID Year": 2020, "Year": "2020", "Population": 331449281, "Slug Nation": "united-states"},
                    {"ID Nation": "01000US", "Nation": "United States", "ID Year": 2021, "Year": "2021", "Population": 331893745, "Slug Nation": "united-states"},
                    {"ID Nation": "01000US", "Nation": "United States", "ID Year": 2022, "Year": "2022", "Population": 333287557, "Slug Nation": "united-states"}
                ],
                "source": "fallback"
            }

async def fetch_coingecko_global() -> Dict[str, Any]:
    """Fetches global cryptocurrency market data from the free CoinGecko API or fallback."""
    url = "https://api.coingecko.com/api/v3/global"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            print("CoinGecko API request failed, using fallback data.")
            return {
                "data": {
                    "active_cryptocurrencies": 14500,
                    "markets": 1200,
                    "total_market_cap": {"usd": 2450000000000},
                    "total_volume": {"usd": 125000000000},
                    "market_cap_percentage": {"btc": 52.5, "eth": 16.2}
                },
                "source": "fallback"
            }

async def fetch_apis_guru_metrics() -> Dict[str, Any]:
    """Fetches API availability density from APIs.guru to demonstrate API Demand."""
    url = "https://api.apis.guru/v2/metrics.json"
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            print("APIs.guru API request failed, using fallback data.")
            return {
                "numAPIs": 2500,
                "numEndpoints": 100000,
                "datasets": [
                    {
                        "title": "providerCount",
                        "data": {
                            "googleapis.com": 350,
                            "azure.com": 200,
                            "amazonaws.com": 180,
                            "microsoft.com": 120,
                            "cisco.com": 80,
                            "ibm.com": 70,
                            "oracle.com": 60,
                            "salesforce.com": 50,
                            "twilio.com": 40,
                            "stripe.com": 35,
                            "Others": 1315
                        }
                    }
                ],
                "source": "fallback"
            }
