# Spec-Driven App Constitution

## Core Principles

### I. Separation of Concerns

Frontend and backend are distinct layers with a clear API boundary. The frontend never accesses the database directly. The backend never renders HTML. All communication between layers happens through a RESTful JSON API.

### II. Localhost-First Development

The entire stack runs locally with no external service dependencies. Use SQLite or a local PostgreSQL/MySQL instance for data persistence. No cloud services, no third-party APIs required to run the app. A single command should start the full stack.

### III. Test-First (NON-NEGOTIABLE)

Tests are written before implementation code. Unit tests cover all business logic and utility functions. API endpoint tests verify request/response contracts. Frontend component tests verify rendering and user interactions. No feature is considered complete without passing tests.

### IV. Explicit Over Implicit

No magic configuration or hidden conventions. Environment variables are documented in a `.env.example` file. All routes are explicitly defined, not auto-generated. Database schemas are version-controlled via migrations. Dependencies are pinned to exact versions in lock files.

### V. Simplicity and Minimalism

Use the minimum number of dependencies to achieve the goal. Avoid frameworks or libraries unless they solve a concrete, immediate problem. No premature abstractions: write the straightforward solution first. Flat file structures preferred over deep nesting. YAGNI: do not build for hypothetical future requirements.

## Technology Constraints

- **Frontend**: HTML, CSS, and JavaScript (or TypeScript). A lightweight framework (e.g., React, Vue, or Svelte) is permitted but not required.
- **Backend**: Python (e.g., FastAPI, Flask, or equivalent lightweight framework).
- **Database**: SQLite for simplicity, or PostgreSQL if relational complexity demands it. No ORMs unless justified; prefer raw SQL or a thin query builder.
- **Package Manager**: uv. The virtual environment (`.venv`) should be used, and dependencies must be tracked via `pyproject.toml` and locked with `uv.lock`.
- **Port Allocation**: Backend API on `localhost:3000`, frontend dev server on `localhost:5173` (or similar). Ports must be configurable via environment variables.
- **No Docker Required**: The app must run without containerization for local development. Docker may be added later but is never a prerequisite.

## Development Workflow

- All work happens on feature branches; `main` is the stable branch.
- Each feature branch maps to a single spec or task from the `.specify/` plan.
- Commits are atomic and descriptive: one logical change per commit.
- Code must pass linting and all tests before merging to `main`.
- Database schema changes require a migration file, never manual edits.
- API changes must update any corresponding API documentation or contract tests.

## Governance

This constitution is the highest authority for project decisions. Any deviation requires an explicit amendment with justification documented here. All code contributions and reviews must verify compliance with these principles. When in doubt, choose the simpler option.

**Version**: 1.0.0 | **Ratified**: 2026-02-22 | **Last Amended**: 2026-02-22
