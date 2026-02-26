# Tasks: Constitution Compliance Audit & Remediation

**Input**: Design documents from `/specs/001-constitution-compliance/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/api-endpoints.md, quickstart.md

**Tests**: Endpoint tests ARE required (FR-003 from spec.md, constitution §III Test-First is NON-NEGOTIABLE).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/`, `frontend/`, `tests/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Ensure `.env` is gitignored and existing tests still pass before making any changes

- [x] T001 Verify `.env` is listed in `.gitignore` (add if missing) in .gitignore
- [x] T002 Run existing test suite to confirm baseline passes: `uv run pytest tests/ -v`

**Checkpoint**: Baseline confirmed — 3 existing tests pass, `.env` is gitignored

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No foundational blocking tasks needed. The existing project structure, dependencies, and configuration are already sufficient. All user stories can begin immediately after Phase 1.

**Checkpoint**: Foundation ready — user story implementation can begin

---

## Phase 3: User Story 1 — API Resilience & Error Safety (Priority: P1) MVP

**Goal**: Add fallback error handling to `fetch_apis_guru_metrics` so all three endpoints respond safely when external APIs are unreachable.

**Independent Test**: Call `GET /api/metrics/api-demand` with the APIs.guru fetcher mocked to raise `httpx.HTTPError`. Response must be HTTP 200 with valid fallback JSON.

### Implementation for User Story 1

- [x] T003 [US1] Add try/except with fallback data to `fetch_apis_guru_metrics` in backend/services/data_fetcher.py — wrap the existing `client.get()` and `raise_for_status()` in a try/except block catching `httpx.HTTPError`, returning a fallback dict with `numAPIs`, `numEndpoints`, and `datasets` (including `providerCount`) matching the shape documented in data-model.md. Add a timeout to the `AsyncClient` constructor (`timeout=5.0`) matching the other fetchers. Add a `"source": "fallback"` key to the fallback response.

**Checkpoint**: `fetch_apis_guru_metrics` now returns fallback data on failure instead of crashing. All 3 existing unit tests still pass.

---

## Phase 4: User Story 2 — Environment Configuration Transparency (Priority: P2)

**Goal**: Create `.env.example` and make HOST/PORT configurable via environment variables so new developers can understand and customize the app configuration.

**Independent Test**: Copy `.env.example` to `.env`, start the server — it runs on the documented default port. Set `PORT=8080`, restart — it runs on 8080.

### Implementation for User Story 2

- [x] T004 [P] [US2] Create `.env.example` at project root with documented HOST and PORT variables — include comments explaining each variable, its type, and its default value per data-model.md env var table
- [x] T005 [US2] Update `backend/main.py` to read HOST and PORT from environment variables using `os.environ.get()` with defaults (`127.0.0.1` and `3000`) per research decision R2 — replace the hardcoded values in the `uvicorn.run()` call at the bottom of the file

**Checkpoint**: `.env.example` exists, HOST/PORT are configurable, app starts with defaults when `.env` is absent.

---

## Phase 5: User Story 3 — Complete Test Coverage for All Endpoints (Priority: P3)

**Goal**: Add HTTP-level endpoint tests for all three API routes using TestClient with mocked fetchers, so the full request/response contract is verified offline.

**Independent Test**: Run `uv run pytest tests/ -v` — at least 6 tests pass (3 existing unit tests + 3 new endpoint tests), all offline.

### Tests for User Story 3

- [x] T006 [P] [US3] Add endpoint test `test_census_endpoint` in tests/test_backend.py — use `from fastapi.testclient import TestClient`, import `app` from `backend.main`, patch `backend.main.fetch_datausa_population` with `AsyncMock` returning census fallback data, call `client.get("/api/census/demographics")`, assert status 200 and response body contains `labels` (list of str) and `datasets` with `population`, `growth`, `growth_pct` keys (each list of numbers) per contracts/api-endpoints.md
- [x] T007 [P] [US3] Add endpoint test `test_crypto_endpoint` in tests/test_backend.py — patch `backend.main.fetch_coingecko_global` with `AsyncMock` returning crypto fallback data, call `client.get("/api/finance/crypto")`, assert status 200 and response body contains `metrics` with keys `active_cryptocurrencies`, `total_markets`, `total_market_cap_usd`, `total_volume_usd`, `btc_dominance_pct` per contracts/api-endpoints.md
- [x] T008 [P] [US3] Add endpoint test `test_api_demand_endpoint` in tests/test_backend.py — patch `backend.main.fetch_apis_guru_metrics` with `AsyncMock` returning APIs.guru fallback data (with `numAPIs`, `numEndpoints`, `datasets` including `providerCount`), call `client.get("/api/metrics/api-demand")`, assert status 200 and response body contains `metrics` with `total_apis` and `total_endpoints`, and `chart_data` with `labels` and `counts` per contracts/api-endpoints.md
- [x] T009 [US3] Run full test suite `uv run pytest tests/ -v` and confirm all 6+ tests pass with zero failures

**Checkpoint**: 6+ tests pass, all offline, covering both unit and endpoint levels. Constitution §III satisfied.

---

## Phase 6: User Story 4 — Single-Command Startup (Priority: P4)

**Goal**: Provide a single documented command to start the full stack locally.

**Independent Test**: Run `uv run start` from project root — server starts and dashboard is accessible at `http://localhost:3000`.

### Implementation for User Story 4

- [x] T010 [US4] Add a startup function and `[project.scripts]` entry in pyproject.toml — create a `start` script entry pointing to a function that calls `uvicorn.run(app, host=host, port=port)` using the env-var-configured values from backend/main.py. The function should be importable (e.g., `backend.main:run_server` or similar pattern compatible with `[project.scripts]`).
- [x] T011 [US4] Update README.md with quickstart instructions — add a "Getting Started" section documenting: (1) `uv sync` to install deps, (2) `cp .env.example .env` (optional), (3) `uv run start` to launch, (4) open `http://localhost:3000`

**Checkpoint**: `uv run start` launches the full stack. README documents the command. Constitution §II satisfied.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final validation across all stories

- [x] T012 Run full test suite one final time: `uv run pytest tests/ -v` — confirm all tests pass
- [x] T013 Verify quickstart.md scenarios: start server with `uv run start`, confirm dashboard loads at `localhost:3000`
- [x] T014 Verify constitution compliance: review all 5 principles against current state — all should now PASS

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: N/A — no blocking prerequisites
- **US1 (Phase 3)**: Can start after Phase 1 — no dependencies on other stories
- **US2 (Phase 4)**: Can start after Phase 1 — no dependencies on other stories
- **US3 (Phase 5)**: Depends on US1 completion (T003 must be done so the APIs.guru fallback exists for testing)
- **US4 (Phase 6)**: Depends on US2 completion (T005 must be done so `uvicorn.run` uses env vars that the startup script leverages)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (P1)**: Independent — can start immediately after Phase 1
- **US2 (P2)**: Independent — can start immediately after Phase 1
- **US3 (P3)**: Depends on US1 (needs the APIs.guru fallback to exist for complete endpoint test coverage)
- **US4 (P4)**: Depends on US2 (needs env-var-configured `uvicorn.run` for the startup script)

### Within Each User Story

- Implementation before integration testing
- Verify after each story completes
- Commit after each task or logical group

### Parallel Opportunities

- **T004 + T003**: US2's `.env.example` creation and US1's fallback fix can run in parallel (different files)
- **T006 + T007 + T008**: All three endpoint tests can be written in parallel (same file but independent test functions — group as single task if preferred)
- **T010 + T011**: Startup script and README update touch different files

---

## Parallel Example: User Stories 1 & 2

```text
# These can run in parallel (different files, no dependencies):
Task T003: Add fallback to fetch_apis_guru_metrics in backend/services/data_fetcher.py
Task T004: Create .env.example at project root

# Then T005 (backend/main.py env vars) after T004
# Then T006-T008 (endpoint tests) after T003
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Verify baseline (T001-T002)
2. Complete Phase 3: US1 — APIs.guru fallback (T003)
3. **STOP and VALIDATE**: All 3 endpoints return valid JSON even when external APIs are down
4. This alone fixes the most critical bug (server crash on network failure)

### Incremental Delivery

1. Phase 1 (Setup) → Baseline confirmed
2. US1 (Fallback fix) → Critical bug resolved
3. US2 (Env config) → Onboarding friction removed
4. US3 (Endpoint tests) → Constitution §III fully satisfied
5. US4 (Startup command) → Constitution §II fully satisfied
6. Phase 7 (Polish) → Full compliance verified

### Task Summary

| Phase | Story | Tasks | Count |
| ----- | ----- | ----- | ----- |
| 1     | Setup | T001-T002 | 2 |
| 2     | Foundational | — | 0 |
| 3     | US1 (P1) | T003 | 1 |
| 4     | US2 (P2) | T004-T005 | 2 |
| 5     | US3 (P3) | T006-T009 | 4 |
| 6     | US4 (P4) | T010-T011 | 2 |
| 7     | Polish | T012-T014 | 3 |
| **Total** | | | **14** |

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Constitution §III (Test-First) is NON-NEGOTIABLE — endpoint tests are mandatory
- Zero new dependencies added across all tasks
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
