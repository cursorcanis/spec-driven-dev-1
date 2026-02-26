# AnalytiQ — Data Analyst Executive Dashboard

A real-time data dashboard that aggregates US population demographics, global cryptocurrency market data, and public API ecosystem metrics into a single executive view.

## Getting Started

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager

### Install dependencies

```bash
uv sync
```

### Configure environment (optional)

```bash
cp .env.example .env
# Edit .env to customize HOST and PORT (defaults: 127.0.0.1:3000)
```

### Start the application

```bash
uv run start
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Run tests

```bash
uv run pytest tests/ -v
```

## Architecture

- **Backend**: FastAPI (Python) serving a JSON API on `localhost:3000`
- **Frontend**: Vanilla HTML/CSS/JS with Chart.js, served as static files
- **Data Sources**: DataUSA, CoinGecko, APIs.guru (all with offline fallbacks)

## Project Structure

```text
backend/          # FastAPI app, services, data fetchers
frontend/         # Static HTML/CSS/JS dashboard
tests/            # Unit and endpoint tests
.env.example      # Environment variable documentation
pyproject.toml    # Dependencies and scripts
```
