# API Endpoint Contracts

**Branch**: `001-constitution-compliance` | **Date**: 2026-02-24

All endpoints return JSON. All endpoints must return HTTP 200 with valid JSON under both normal and degraded (no network) conditions.

## GET /api/health

**Purpose**: Liveness check
**Response**: `{"status": "ok"}`

---

## GET /api/census/demographics

**Purpose**: US population data with year-over-year growth
**Data source**: DataUSA API (with fallback)

**Success response**:

```json
{
  "labels": ["2018", "2019", "2020", "2021", "2022"],
  "datasets": {
    "population": [327167434, 328239523, 331449281, 331893745, 333287557],
    "growth": [0.0, 1072089.0, 3209758.0, 444464.0, 1393812.0],
    "growth_pct": [0.0, 0.33, 0.98, 0.13, 0.42]
  }
}
```

**Assertions**:
- Status code: 200
- Body contains `labels` (list of strings)
- Body contains `datasets` with keys `population`, `growth`, `growth_pct` (each a list of numbers)

---

## GET /api/finance/crypto

**Purpose**: Global cryptocurrency market summary
**Data source**: CoinGecko API (with fallback)

**Success response**:

```json
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

**Assertions**:
- Status code: 200
- Body contains `metrics` with keys: `active_cryptocurrencies`, `total_markets`, `total_market_cap_usd`, `total_volume_usd`, `btc_dominance_pct`

---

## GET /api/metrics/api-demand

**Purpose**: Public API ecosystem metrics and top provider distribution
**Data source**: APIs.guru (with fallback — currently missing, to be added)

**Success response**:

```json
{
  "metrics": {
    "total_apis": 2500,
    "total_endpoints": 100000
  },
  "chart_data": {
    "labels": ["googleapis.com", "azure.com"],
    "counts": [350, 200]
  }
}
```

**Assertions**:
- Status code: 200
- Body contains `metrics` with keys: `total_apis`, `total_endpoints`
- Body contains `chart_data` with keys: `labels` (list of strings), `counts` (list of numbers)
