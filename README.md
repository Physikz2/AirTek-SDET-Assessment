# JSONPlaceholder API Test Automation Framework

![Build Status](https://github.com/Physikz2/AirTek-SDET-Assessment/actions/workflows/test.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Framework-Pytest-0A9EDC?logo=pytest&logoColor=white)
![Pydantic](https://img.shields.io/badge/Validation-Pydantic%20v2-E92063?logo=pydantic&logoColor=white)
![Requests](https://img.shields.io/badge/HTTP-Requests-3776AB?logo=python&logoColor=white)
![HTML Reports](https://img.shields.io/badge/Reporting-pytest--html-22A559)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)

An enterprise-grade API test automation framework targeting all six JSONPlaceholder endpoints (`/posts`, `/comments`, `/albums`, `/photos`, `/todos`, `/users`). Built with Python, Pytest, Pydantic v2, and Requests.

---

## 🛠️ Tech Stack & Architectural Usage

| Technology / Tool | Badge | Strategic Engineering Role |
| :--- | :--- | :--- |
| **Python 3.10+** | ![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white) | Core language providing strict type hinting, efficient runtime, and clean object-oriented architecture. |
| **Pytest** | ![Pytest](https://img.shields.io/badge/Framework-Pytest-0A9EDC?logo=pytest&logoColor=white) | Test execution engine utilizing `@pytest.mark.parametrize` for data-driven coverage and `conftest.py` for dynamic fixtures. |
| **Pydantic v2** | ![Pydantic](https://img.shields.io/badge/Validation-Pydantic%20v2-E92063?logo=pydantic&logoColor=white) | Strict contract and schema validation layer ensuring structural type safety (`extra='ignore'`) across REST responses. |
| **Requests** | ![Requests](https://img.shields.io/badge/HTTP-Requests-3776AB?logo=python&logoColor=white) | Low-level HTTP transport wrapped in a persistent `requests.Session` class for TCP connection reuse and latency logging. |
| **pytest-html** | ![HTML Reports](https://img.shields.io/badge/Reporting-pytest--html-22A559) | Visual dashboard generation engine that packages test metrics and step logs into a standalone `report.html` file. |
| **GitHub Actions** | ![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white) | Automated continuous integration pipeline triggering full regression runs and uploading visual HTML build artifacts. |

---

## 🏛️ System Architecture & Design Principles

- **`client/api_client.py`**: Encapsulates a persistent `requests.Session`, centralizes HTTP verbs (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`), handles standard timeouts, and tracks millisecond latency (`time.perf_counter()`).
- **`config/settings.py`**: Manages environment variables and CLI parameters for multi-environment switching (`--env prod|staging|dev`).
- **`models/`**: Defines Pydantic v2 schemas for contract testing, enforcing field types and sub-document validation while tolerating non-breaking schema additions.
- **`tests/`**: Separates test modules into logical concerns: route availability, strict schema validation, full CRUD lifecycles, relational query routes, and negative 404 paths.
- **`pytest.ini`**: Configures framework defaults, enabling live `INFO` latency logging and auto-generating the self-contained `report.html` dashboard.

---

## 🚀 Setup & Installation

    # Clone the repository
    git clone https://github.com/YOUR_GITHUB_USERNAME/AirTek-SDET-Assessment.git
    cd AirTek-SDET-Assessment

    # Create and activate virtual environment
    python -m venv .venv
    .venv\Scripts\activate  # Windows
    # source .venv/bin/activate  # macOS/Linux

    # Install dependencies
    pip install -r requirements.txt

---

## 🧪 Running Tests & Multi-Environment CLI

Execute the default suite against the production JSONPlaceholder deployment:

    pytest

Run tests against specific environment targets:

    pytest --env prod
    pytest --env staging
    pytest --env dev

> **Note on Environment Aliases:** Because JSONPlaceholder is a public mock API without isolated staging environments, all aliases currently route to the primary production host. This preserves CLI command-line compatibility for enterprise CI pipelines.

### Focused Test Execution

    # Run route availability tests
    pytest tests/test_all_routes.py -q

    # Run schema validation tests
    pytest tests/test_schemas.py -q

    # Run CRUD lifecycle tests
    pytest tests/test_crud.py -q

---

## 📊 Coverage Matrix

| Resource / Endpoint | GET Collection | GET by ID / Nested | POST | PUT | PATCH | DELETE | Pydantic Contract Validation |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `/posts` | ✅ | ✅ (`/posts/1/comments`) | ✅ | ✅ | ✅ | ✅ | `Post`, `PostCreate` |
| `/comments` | ✅ | ✅ (`?postId=1`) | — | — | — | — | `Comment` |
| `/albums` | ✅ | ✅ | — | — | — | — | `Album` |
| `/photos` | ✅ | ✅ | — | — | — | — | `Photo` |
| `/todos` | ✅ | ✅ | — | — | — | — | `Todo` |
| `/users` | ✅ | ✅ | — | — | — | — | `User`, `Address`, `Geo`, `Company` |
| **Invalid Paths** | — | ✅ (404 Boundary Checks) | — | — | — | — | Status Code Contract |

---

## 📈 Latency Logging & Visual Reporting

Every API interaction records response metrics in real-time:

    INFO - GET /posts | Status: 200 | Latency: 172.29ms
    INFO - POST /posts | Status: 201 | Latency: 64.12ms

Upon test completion, `pytest-html` automatically compiles an interactive execution report saved directly to `report.html`.

In GitHub Actions CI/CD, this dashboard is uploaded automatically as an artifact named `api-test-report`.

---

## ⚡ Engineering Trade-offs & Strategic Omissions

1. **Mock Persistence Constraints:** JSONPlaceholder simulates write operations (`POST`, `PUT`, `PATCH`, `DELETE`) by returning HTTP success status codes and echoing payloads without mutating real backend state. CRUD tests validate headers, payload echo attributes, and status codes rather than downstream state persistence.
2. **Execution Efficiency:** Broad surface area validation is prioritized over slow, non-deterministic performance testing. Load testing, concurrency checks, and authentication flows are deliberately omitted as they fall outside the scope of a public simulated API service.

## 📖 Operations & Execution Guide
For detailed instructions on dynamic CLI flags, live logging, isolated test filtering, and troubleshooting, see the [RUN_GUIDE.md](./RUN_GUIDE.md).