# Implementation Plan: Constitution Compliance Audit & Remediation

**Branch**: `001-constitution-compliance` | **Date**: 2026-02-24 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-constitution-compliance/spec.md`

## Summary

Bring the existing Data Analyst Dashboard into full compliance with the project constitution. Four gaps exist: (1) the APIs.guru fetcher lacks error handling and crashes on network failure, (2) no `.env.example` documents configurable environment variables, (3) no HTTP-level endpoint tests exist (only unit tests for two processors), and (4) no single documented startup command exists. Each gap maps to a specific constitutional principle violation and will be resolved with minimal, targeted changes.

## Technical Context

**Language/Version**: Python 3.11 (via uv, `.python-version` pinned)
**Primary Dependencies**: FastAPI 0.131+, httpx 0.28+, pandas 3.0+, uvicorn 0.41+
**Storage**: N/A (no database — all data fetched from external APIs with fallbacks)
**Testing**: pytest 9.0+ with `pythonpath = ["."]` in pyproject.toml; FastAPI TestClient via httpx
**Target Platform**: localhost (Windows 11, cross-platform compatible)
**Project Type**: Web application (FastAPI backend serving static HTML/CSS/JS frontend)
**Performance Goals**: Dashboard loads within 5 seconds; fallbacks respond immediately on network failure
**Constraints**: Offline-capable for tests; no external service required to run; uv as package manager
**Scale/Scope**: Single-developer project, 3 API endpoints, 1 static frontend

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Detail |
| --------- | ------ | ------ |
| **§I Separation of Concerns** | PASS | Frontend is static HTML/JS/CSS served by StaticFiles mount. Backend is pure JSON API. No HTML rendering in backend. |
| **§II Localhost-First** | FAIL → remediate | App runs locally but: (a) `fetch_apis_guru_metrics` has no fallback — crashes without network; (b) no single startup command documented. |
| **§III Test-First** | FAIL → remediate | Unit tests exist for 2 of 3 processors. No HTTP-level endpoint tests. No test for `process_apis_guru_metrics`. |
| **§IV Explicit Over Implicit** | FAIL → remediate | No `.env.example`. Port 3000 is hardcoded in `backend/main.py`. Routes are explicit (PASS). Dependencies locked via `uv.lock` (PASS). |
| **§V Simplicity** | PASS | Minimal dependencies. Flat structure. No premature abstractions. |
| **Technology Constraints** | PASS | Python/FastAPI backend, HTML/CSS/JS frontend, uv package manager, port 3000. All aligned. |
| **Development Workflow** | PASS (in progress) | Working on feature branch `001-constitution-compliance`. Atomic commits planned. |

**Gate result**: 3 violations found — all are the remediation targets for this feature. No unjustified violations. Proceed.

## Project Structure

### Documentation (this feature)

```text
specs/001-constitution-compliance/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── api-endpoints.md # Endpoint contracts for all 3 routes + health
└── tasks.md             # Phase 2 output (via /speckit.tasks)
```

### Source Code (repository root)

```text
backend/
├── __init__.py
├── main.py              # FastAPI app, routes, static mount
└── services/
    ├── data_fetcher.py  # 3 async fetchers (MODIFY: add fallback to APIs.guru)
    └── data_analyzer.py # 3 processors (no changes needed)

frontend/
├── index.html           # Dashboard layout
├── styles.css           # Styling
└── app.js               # Chart.js rendering

tests/
└── test_backend.py      # Existing unit tests (MODIFY: add endpoint tests)

.env.example             # NEW: environment variable documentation
main.py                  # Entry point (exists, may update for env var loading)
pyproject.toml           # Dependencies and pytest config
```

**Structure Decision**: Existing web application structure is already correct and constitution-compliant. No structural changes needed — only targeted file modifications and one new file (`.env.example`).

## Complexity Tracking

> No violations requiring justification. All changes are remediation of constitution gaps.

| Violation | Why Needed | Simpler Alternative Rejected Because |
| --------- | ---------- | ------------------------------------ |
| N/A       | —          | —                                    |

## Constitution Re-Check (Post-Design)

*Re-evaluated after Phase 1 design artifacts are complete.*

| Principle | Status | Detail |
| --------- | ------ | ------ |
| **§I Separation of Concerns** | PASS | No change. Design adds no new coupling between frontend and backend. |
| **§II Localhost-First** | WILL PASS | Design adds APIs.guru fallback (R3) and single-command startup via `uv run start` (R4). Zero new external dependencies. |
| **§III Test-First** | WILL PASS | Design adds 3 HTTP-level endpoint tests using TestClient + AsyncMock (R1). All tests run offline. No new test dependencies. |
| **§IV Explicit Over Implicit** | WILL PASS | Design adds `.env.example` and makes HOST/PORT configurable via `os.environ.get()` (R2). No magic. |
| **§V Simplicity** | PASS | Zero new dependencies added. All changes use stdlib (`os`, `unittest.mock`) and existing packages. Fallback pattern matches existing code. |
| **Technology Constraints** | PASS | No change. All design decisions use the existing stack. |
| **Development Workflow** | PASS | Feature branch active. Atomic commits planned per task. |

**Post-design gate result**: All principles will be satisfied after implementation. No new violations introduced. Design is ready for task generation.
