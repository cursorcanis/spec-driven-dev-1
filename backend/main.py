import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="Data Analyst Dashboard API")

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

from backend.services.data_fetcher import fetch_datausa_population, fetch_coingecko_global, fetch_apis_guru_metrics
from backend.services.data_analyzer import process_census_data, process_coingecko_data, process_apis_guru_metrics

# Endpoints for our 3 designated data sources
@app.get("/api/census/demographics")
async def get_census_data():
    raw_data = await fetch_datausa_population()
    processed_data = process_census_data(raw_data)
    return processed_data

@app.get("/api/metrics/api-demand")
async def get_api_demand():
    raw_data = await fetch_apis_guru_metrics()
    processed_data = process_apis_guru_metrics(raw_data)
    return processed_data

@app.get("/api/finance/crypto")
async def get_crypto_trends():
    raw_data = await fetch_coingecko_global()
    processed_data = process_coingecko_data(raw_data)
    return processed_data

# Mount the frontend directory to serve static HTML/JS/CSS
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
try:
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
except RuntimeError as e:
    print(f"Frontend directory not mounted: {e}")

def run_server():
    """Entry point for `uv run start`."""
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "3000"))
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    run_server()
