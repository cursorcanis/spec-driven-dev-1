import pandas as pd
from typing import Dict, Any

def process_census_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Cleans and structures 'Data USA' population data for charting.
    Expected raw format: {"data": [{"ID Nation": "01000US", "Nation": "United States", "ID Year": 2022, "Year": "2022", "Population": 331002647, "Slug Nation": "united-states"}, ...]}
    """
    if not raw_data or "data" not in raw_data:
        return {"error": "Invalid data format"}
    
    # Load into a pandas DataFrame
    df = pd.DataFrame(raw_data["data"])
    
    # Filter for relevant columns
    df = df[["Year", "Population"]]
    
    # Sort chronologically
    df["Year"] = pd.to_numeric(df["Year"])
    df = df.sort_values(by="Year", ascending=True)
    
    # Calculate Year-over-Year Growth
    df["YoY_Growth"] = df["Population"].diff()
    df["YoY_Growth_Pct"] = df["Population"].pct_change() * 100
    
    # Fill NaN from diff with 0
    df = df.fillna(0)
    
    # Return in a format easy for Chart.js to consume
    return {
        "labels": df["Year"].astype(str).tolist(),
        "datasets": {
            "population": df["Population"].tolist(),
            "growth": df["YoY_Growth"].tolist(),
            "growth_pct": df["YoY_Growth_Pct"].round(2).tolist(),
        }
    }

def process_coingecko_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts relevant top-level economy/crypto market cap numbers from CoinGecko global data.
    """
    if not raw_data or "data" not in raw_data:
        return {"error": "Invalid data format"}
    
    data = raw_data["data"]
    
    active_crypto = data.get("active_cryptocurrencies", 0)
    markets = data.get("markets", 0)
    
    # Total market cap (using USD)
    market_cap_usd = data.get("total_market_cap", {}).get("usd", 0)
    volume_usd = data.get("total_volume", {}).get("usd", 0)
    btc_dominance = data.get("market_cap_percentage", {}).get("btc", 0)
    
    return {
        "metrics": {
            "active_cryptocurrencies": active_crypto,
            "total_markets": markets,
            "total_market_cap_usd": market_cap_usd,
            "total_volume_usd": volume_usd,
            "btc_dominance_pct": round(btc_dominance, 2)
        }
    }

def process_apis_guru_metrics(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Structures the APIs.guru metrics to show API ecosystem size and top providers.
    """
    data_block = raw_data.get("data", raw_data)
    
    if "numAPIs" not in data_block:
        return {"error": "Invalid data format"}
        
    # Extract real provider distribution metrics from the datasets array
    provider_data = {}
    datasets = data_block.get("datasets", [])
    for ds in datasets:
        if ds.get("title") == "providerCount":
            provider_data = ds.get("data", {})
            break
            
    # Sort and take top 10 providers (excluding 'Others' for clarity if preferred, but we'll leave it out of the slice)
    # Filter out 'Others' first
    filtered_providers = {k: v for k, v in provider_data.items() if k != "Others"}
    sorted_providers = sorted(filtered_providers.items(), key=lambda item: item[1], reverse=True)[:10]
    
    labels = [k for k, v in sorted_providers]
    counts = [v for k, v in sorted_providers]
    
    return {
        "metrics": {
            "total_apis": data_block.get("numAPIs"),
            "total_endpoints": data_block.get("numEndpoints")
        },
        "chart_data": {
            "labels": labels,
            "counts": counts
        }
    }
