# Data Model: Constitution Compliance Audit & Remediation

**Branch**: `001-constitution-compliance` | **Date**: 2026-02-24

## Overview

This feature does not introduce new data entities or persistence. It remediates gaps in existing behavior. The data structures below document the **existing response shapes** that endpoint tests must assert against, and the **new fallback shape** for the APIs.guru fetcher.

## Existing Response Schemas

### Census Demographics Response

Returned by `GET /api/census/demographics` via `process_census_data`:

```
{
  "labels": ["2018", "2019", ...],
  "datasets": {
    "population": [327167434, 328239523, ...],
    "growth": [0.0, 1072089.0, ...],
    "growth_pct": [0.0, 0.33, ...]
  }
}
```

Error shape: `{"error": "Invalid data format"}`

### Crypto Finance Response

Returned by `GET /api/finance/crypto` via `process_coingecko_data`:

```
{
  "metrics": {
    "active_cryptocurrencies": 14500,
    "total_markets": 1200,
    "total_market_cap_usd": 2450000000000,
    "total_volume_usd": 125000000000,
    "btc_dominance_pct": 52.5
  }
}
```

Error shape: `{"error": "Invalid data format"}`

### API Demand Response

Returned by `GET /api/metrics/api-demand` via `process_apis_guru_metrics`:

```
{
  "metrics": {
    "total_apis": 2500,
    "total_endpoints": 100000
  },
  "chart_data": {
    "labels": ["googleapis.com", "azure.com", ...],
    "counts": [350, 200, ...]
  }
}
```

Error shape: `{"error": "Invalid data format"}`

## New: APIs.guru Fallback Data Shape

The fallback data returned by `fetch_apis_guru_metrics` on network failure must match the shape expected by `process_apis_guru_metrics`. Required fields:

```
{
  "numAPIs": <int>,
  "numEndpoints": <int>,
  "datasets": [
    {
      "title": "providerCount",
      "data": {
        "<provider_name>": <int>,
        ...
      }
    }
  ]
}
```

This ensures the processor can extract `numAPIs`, `numEndpoints`, and the top-10 provider distribution from fallback data identically to live data.

## Environment Variables

| Variable | Type   | Default       | Description                    |
| -------- | ------ | ------------- | ------------------------------ |
| HOST     | string | `127.0.0.1`   | Server bind address            |
| PORT     | int    | `3000`        | Server port                    |
