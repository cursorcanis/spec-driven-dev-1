# Research: Constitution Compliance Audit & Remediation

**Branch**: `001-constitution-compliance` | **Date**: 2026-02-24

## R1: HTTP-Level Endpoint Testing Strategy

**Decision**: Use FastAPI's synchronous `TestClient` with `unittest.mock.patch` + `AsyncMock` for mocking async fetchers. No new dependencies needed.

**Rationale**:
- `from fastapi.testclient import TestClient` is the canonical import (re-exports Starlette's TestClient)
- TestClient is synchronous — it manages its own event loop internally via `anyio`, so test functions are plain `def test_*()`, not async
- All dependencies already satisfied: `httpx` and `anyio` are transitive deps of the existing stack
- `pytest-asyncio` is NOT needed and would add unnecessary complexity / potential event loop conflicts

**Mock pattern**: Patch at `backend.main.<function_name>` (where the name is imported), not at the original `backend.services.data_fetcher.<function_name>`. Use `new_callable=AsyncMock` so the mock is awaitable inside async endpoint handlers.

**Alternatives considered**:
- `pytest-asyncio` + `httpx.AsyncClient`: Unnecessary — sync TestClient already handles async endpoints. Would add a dependency.
- Mocking at `backend.services.data_fetcher.*`: Wrong target — Python's `unittest.mock.patch` requires patching where the name is looked up, which is `backend.main`.

---

## R2: Environment Variable Configuration

**Decision**: Use `os.environ.get()` with sensible defaults. No new dependency (no `python-dotenv`, no `pydantic-settings`).

**Rationale**:
- Constitution §V (Simplicity): "Use the minimum number of dependencies." For 2 variables (HOST, PORT), `os.environ.get()` is sufficient.
- Neither FastAPI nor uvicorn has built-in `.env` file loading
- `python-dotenv` is ~900 lines for a problem that doesn't exist with only 2 env vars
- Developers who want `.env` auto-loading can use IDE support (VS Code auto-loads), `direnv`, or shell-level tools

**Configuration approach**:
- `HOST` defaults to `127.0.0.1`
- `PORT` defaults to `3000`
- Missing `.env` is fine — app starts with defaults (aligns with "single command starts the stack")
- `.env.example` is checked into git as documentation; `.env` is gitignored

**Alternatives considered**:
- `python-dotenv`: Adds a dependency for 2 variables. Rejected per §V.
- `pydantic-settings`: Even heavier (pulls in `python-dotenv` transitively). Overkill for this scope.
- Fail-fast on missing `.env`: Rejected — would break "single command starts full stack" principle.

---

## R3: APIs.guru Fetcher Fallback Pattern

**Decision**: Add a try/except with fallback data to `fetch_apis_guru_metrics`, matching the existing pattern used by the other two fetchers.

**Rationale**:
- `fetch_datausa_population` and `fetch_coingecko_global` already wrap their HTTP calls in try/except and return fallback dictionaries on `httpx.HTTPError`
- `fetch_apis_guru_metrics` is the only fetcher without this pattern — it raises on any network failure
- Consistency: all three fetchers should behave identically under failure
- The fallback data should match the shape of a real APIs.guru response so `process_apis_guru_metrics` processes it correctly

**Alternatives considered**:
- Global exception handler in FastAPI: Would mask the root cause. Better to handle at the fetcher level where fallback data is meaningful.
- Retry logic: Over-engineering for a dashboard with fallback data. Constitution §V applies.

---

## R4: Single-Command Startup

**Decision**: Add a `uv run` script entry point in `pyproject.toml` so `uv run start` launches the server. Document in README.

**Rationale**:
- Constitution §II requires "a single command should start the full stack"
- `uv run` is the project's package manager and already available
- A `[project.scripts]` entry in `pyproject.toml` is the standard Python way to define entry points
- Simpler than adding a Makefile or justfile (§V Simplicity)

**Alternatives considered**:
- `Makefile`: Works but adds a build system dependency. `uv run` is already present.
- `justfile`: Requires installing `just`. Extra tool for one command.
- Raw `python -m uvicorn`: Works but not discoverable. A named script is more explicit (§IV).
