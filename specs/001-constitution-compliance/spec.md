# Feature Specification: Constitution Compliance Audit & Remediation

**Feature Branch**: `001-constitution-compliance`
**Created**: 2026-02-24
**Status**: Draft
**Input**: User description: "this project to make sure it is within the spec kit parameters and adheres to the constitution.md"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - API Resilience & Error Safety (Priority: P1)

As a developer running the application, all three backend data endpoints must respond safely under any external condition — including external API failures. Currently the APIs.guru fetcher has no fallback and will crash the process on network failure, whereas the other two fetchers have proper fallbacks.

**Why this priority**: A crashing endpoint breaks the entire dashboard for end-users. This is a correctness and reliability issue that blocks confident use of the app.

**Independent Test**: Start the server with network access blocked for APIs.guru. Call `/api/metrics/api-demand`. The endpoint must return a structured fallback response, not raise an unhandled exception.

**Acceptance Scenarios**:

1. **Given** the APIs.guru external service is unreachable, **When** a user loads the dashboard, **Then** the API demand panel shows fallback/placeholder data with no server crash or 500 error
2. **Given** any of the three external APIs returns an error, **When** the corresponding endpoint is called, **Then** the response is a valid JSON object (either real or fallback data) with HTTP 200

---

### User Story 2 - Environment Configuration Transparency (Priority: P2)

As a new developer onboarding to the project, I need a documented `.env.example` file so I can understand all required environment variables before running the app locally. The constitution (§IV) explicitly requires this, and it does not currently exist.

**Why this priority**: Without it, new contributors have no way to know what configuration the app expects — violating the Explicit Over Implicit principle.

**Independent Test**: Open the repo fresh, copy `.env.example` to `.env`, follow the instructions, and start the server — the app must run without requiring any undocumented configuration.

**Acceptance Scenarios**:

1. **Given** the project is cloned fresh, **When** a developer copies `.env.example` to `.env`, **Then** the server starts correctly on the documented port with no missing variable errors
2. **Given** a `.env.example` exists, **When** a developer reviews it, **Then** every configurable value (port, host, etc.) is present and documented with a comment

---

### User Story 3 - Complete Test Coverage for All Endpoints (Priority: P3)

As a developer, I need HTTP-level API tests for all three backend endpoints (not just unit tests for the data processors), so that the full request/response contract is verified. The constitution (§III) requires endpoint tests; currently only unit tests for two processor functions exist.

**Why this priority**: Unit tests alone don't catch routing bugs, missing imports, or middleware issues. Endpoint-level tests are required by the constitution and increase confidence when refactoring.

**Independent Test**: Run the test suite. All three API endpoint tests pass without a running external network (using mocked or fallback data).

**Acceptance Scenarios**:

1. **Given** the test suite is run, **When** the test runner executes, **Then** all three endpoints (`/api/census/demographics`, `/api/finance/crypto`, `/api/metrics/api-demand`) have at least one passing HTTP-level test
2. **Given** a test calls an endpoint, **When** the response is received, **Then** the test asserts the response status is 200 and the response body matches the documented schema
3. **Given** all tests run, **When** the suite completes, **Then** zero tests fail and no warnings about missing coverage are present

---

### User Story 4 - Single-Command Startup (Priority: P4)

As a developer, I want to start the entire application (backend serving the frontend) with a single documented command, as required by the constitution (§II: "A single command should start the full stack"). There is currently no `Makefile`, `justfile`, or documented run command beyond the raw `uvicorn` invocation.

**Why this priority**: The constitution mandates single-command startup for localhost-first development. This reduces friction for any developer running the project.

**Independent Test**: From a fresh terminal in the project root, run the documented command. The app is accessible at `http://localhost:3000` within 5 seconds.

**Acceptance Scenarios**:

1. **Given** a developer is in the project root, **When** they run the documented single command, **Then** the backend starts and the frontend is accessible at `localhost:3000`
2. **Given** the app is running, **When** a browser opens `localhost:3000`, **Then** the dashboard renders correctly with no 404 or routing errors

---

### Edge Cases

- What happens when all three external APIs are unreachable simultaneously? The dashboard must still render with fallback data for each panel.
- What happens if `.env` is missing entirely? The app must either start with safe defaults or fail fast with a clear, human-readable error message.
- What happens if tests are run without a network connection? All tests must pass using offline/mock data only.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The APIs.guru data fetcher MUST handle network errors and return structured fallback data instead of raising an unhandled exception
- **FR-002**: A `.env.example` file MUST exist at the project root documenting all configurable environment variables (at minimum: host, port)
- **FR-003**: The project MUST include HTTP-level endpoint tests for all three API routes that pass without external network access
- **FR-004**: The project MUST provide a single documented command (or script) to start the full stack locally
- **FR-005**: All existing unit tests MUST continue to pass after any changes made for compliance
- **FR-006**: The test suite MUST be runnable entirely offline (no external network calls during test execution)

### Key Entities

- **Data Endpoint**: A backend route that fetches from an external source, processes the data, and returns a structured JSON response — must have both a live path and a fallback path
- **Environment Variable**: A named configurable value that controls runtime behavior (e.g., port, host) — must be declared in `.env.example` with a description and default value
- **Endpoint Test**: An HTTP-level test that sends a request to a live application route and asserts on the status code and response body shape

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All three API endpoints return valid JSON with HTTP 200 under both normal and degraded (no network) conditions
- **SC-002**: A developer can onboard and run the project locally using only the README and `.env.example` — zero undocumented steps required
- **SC-003**: The test suite includes at least 6 passing tests (3 existing unit tests + 3 new endpoint-level tests) and completes in under 30 seconds
- **SC-004**: Every gap identified in the constitution compliance audit is resolved and traceable to a specific requirement in this spec
- **SC-005**: The full test suite passes with zero failures on a machine with no external network access
