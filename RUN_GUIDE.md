# AirTek SDET Assessment — Execution & Operations Guide

This guide details all execution patterns, CLI flags, environment setup steps, and directory-level contexts required to run the API Test Automation Suite.

---

## 1. Prerequisites & Virtual Environment Setup

Always verify that your virtual environment is created and activated before executing test commands.

### Step-by-Step Setup
Execute these commands from the **root directory** (`C:\Projects\AirTek-SDET-Assessment`):

1. **Create Virtual Environment:**
   python -m venv .venv

2. **Activate Virtual Environment:**
   * **Windows (PowerShell):**
     .venv\Scripts\Activate.ps1
   * **Windows (CMD):**
     .venv\Scripts\activate.bat
   * **macOS / Linux:**
     source .venv/bin/activate

3. **Install Dependencies:**
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt

---

## 2. Directory Context & Execution Rules

* **Primary Execution Directory:** All commands **MUST** be run from the repository **root folder** (`AirTek-SDET-Assessment/`).
* **Why use `python -m pytest`?** 
  Running `python -m pytest` forces Python to execute the `pytest` package installed directly inside `.venv/`, ensuring `sys.path` includes the root directory. This prevents `ModuleNotFoundError` when importing local packages (`client`, `config`, `models`).

---

## 3. Test Execution Commands

### Standard Full Suite Execution
Run the entire test suite and automatically generate/overwrite `report.html`:
python -m pytest

### Real-Time Live Terminal Logging
Print HTTP request methods, URLs, status codes, and millisecond latency directly to standard output while tests execute:
python -m pytest -o log_cli=true --log-cli-level=INFO

### Generate Standalone HTML Report
Explicitly generate a single self-contained HTML report (useful for sharing offline):
python -m pytest --html=report.html --self-contained-html

---

## 4. Target Isolation & Filtering

### Run a Single Test File
* **Run only CRUD operations:**
  python -m pytest tests/test_crud.py

* **Run only schema/Pydantic validation tests:**
  python -m pytest tests/test_schemas.py

* **Run only negative/error path tests:**
  python -m pytest tests/test_negative.py

* **Run only relationship integrity tests:**
  python -m pytest tests/test_relations.py

* **Run only route availability tests:**
  python -m pytest tests/test_all_routes.py

### Run a Specific Test Function
Target an individual test function across the entire suite using `-k`:
* **Run only tests matching "posts":**
  python -m pytest -k "posts"

* **Run a specific CRUD test by function name:**
  python -m pytest -k "test_create_post"

### Re-running Failures
* **Run Only Last Failed Tests (`--lf`):**
  python -m pytest --lf

* **Run Failed Tests First, Then Rest of Suite (`--ff`):**
  python -m pytest --ff

---

## 5. Dynamic CLI Parameterization & Environment Overrides

The suite supports dynamic configuration overrides via `conftest.py` CLI options and environment variables managed in `config/settings.py`.

### Override Base URL via CLI Flag
Target a specific environment (e.g., staging or local mock server) dynamically:
python -m pytest --base-url="https://jsonplaceholder.typicode.com"

### Target Specific Environments (`--env`)
* **Run against Staging:**
  python -m pytest --env staging

* **Run against Production:**
  python -m pytest --env prod

### Override Request Timeout
Modify default HTTP request timeouts (in seconds) for slow networks or SLA regression testing:
python -m pytest --timeout=5

---

## 6. Framework Verification & Diagnostics

### List Discovered Tests Without Executing
Verify that Pytest can parse all test files and fixtures correctly:
python -m pytest --collect-only

### Inspect Installed Package Versions
Confirm all dependencies match `requirements.txt`:
pip list

### Clean Up Pytest Cache & Artifacts
If experiencing local cache conflicts, clear local execution cache:
* **Windows PowerShell:**
  Remove-Item -Recurse -Force .pytest_cache, report.html -ErrorAction SilentlyContinue

* **macOS / Linux / Git Bash:**
  rm -rf .pytest_cache report.html

---

## 7. Quick Interview Reference Cheatsheet

* **"Where do I run commands?"** -> From the repository root (`AirTek-SDET-Assessment/`).
* **"How do I see live latency logs?"** -> `python -m pytest -o log_cli=true --log-cli-level=INFO`
* **"How do I run a single test?"** -> `python -m pytest tests/test_crud.py -k "test_create_post"`
* **"How do I run only failed tests?"** -> `python -m pytest --lf`
* **"How do I target another environment?"** -> `python -m pytest --base-url="https://staging-api.example.com"`