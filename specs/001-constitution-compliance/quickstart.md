# Quickstart: Constitution Compliance Changes

**Branch**: `001-constitution-compliance` | **Date**: 2026-02-24

## What Changes

This feature makes 4 targeted changes to bring the project into constitution compliance:

### 1. Add fallback to APIs.guru fetcher

**File**: `backend/services/data_fetcher.py`
**Change**: Wrap `fetch_apis_guru_metrics` in try/except matching the pattern of the other two fetchers. Return structured fallback data on `httpx.HTTPError`.

### 2. Create `.env.example`

**File**: `.env.example` (new file at project root)
**Change**: Document `HOST` and `PORT` variables with defaults and comments. Update `backend/main.py` to read from `os.environ.get()` instead of hardcoded values.

### 3. Add HTTP-level endpoint tests

**File**: `tests/test_backend.py`
**Change**: Add 3 endpoint tests using `FastAPI.TestClient`. Each test mocks the async fetcher with `AsyncMock` to avoid network calls, then asserts status 200 and response body shape per the contracts in `contracts/api-endpoints.md`.

### 4. Document single-command startup

**File**: `pyproject.toml` (add script entry), `README.md` (update)
**Change**: Add a `[project.scripts]` entry so `uv run start` launches the server. Update README with the command.

## How to Verify

```bash
# Run all tests (should be 6+ passing, all offline)
uv run pytest tests/ -v

# Start the app
uv run start
# Then open http://localhost:3000

# Verify with custom port
PORT=8080 uv run start
# Then open http://localhost:8080
```

## Dependencies

No new dependencies are added. All changes use existing stdlib (`os`, `unittest.mock`) and installed packages (`fastapi`, `httpx`, `pytest`).
