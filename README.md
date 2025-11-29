# Emerald Ledger API

## Project Overview

**Emerald Ledger** is a FastAPI-based backend application for managing emerald inventory, counterparty relationships, and trading transactions. The system provides comprehensive CRUD operations for three core entities:

- **Emeralds**: Track individual emerald lots with gemological properties (carat, shape, color grade, clarity, treatment, origin, certificate ID, and status)
- **Counterparties**: Manage suppliers, buyers, and brokers with contact information, country, and KYC notes
- **Trades**: Record purchase and sale transactions with financial details, dates, and relationships to emeralds and counterparties

The application uses **SQLAlchemy ORM** with SQLite for data persistence, **Pydantic** for request/response validation, and includes comprehensive business logic for inventory management and financial reporting.

**Technologies:**
- **Backend Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0
- **Database**: SQLite (with foreign key constraints enabled)
- **Validation**: Pydantic v2
- **Containerization**: Docker
- **Cloud Deployment**: Azure Container Registry (ACR), Azure Web App
- **CI/CD**: GitHub Actions

---

## Local Development Setup

### Prerequisites
- Python 3.12+
- pip (Python package manager)

### Step 1: Create and Activate Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
# .venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

The `requirements.txt` includes:
- `fastapi>=0.104.0`
- `uvicorn[standard]>=0.24.0`
- `sqlalchemy>=2.0.0`
- `pydantic>=2.8.0`
- `pytest>=7.4.0`
- `pytest-cov>=4.1.0`
- `httpx>=0.25.0`

### Step 3: Initialize Database

The database is automatically created when the application starts (via `Base.metadata.create_all()` in `database.py`). The SQLite database file `emerald.db` will be created in the project root.

### Step 4: Run the Application Locally

```bash
# Start the FastAPI server with auto-reload
uvicorn main:app --reload
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive API Documentation (Swagger)**: http://localhost:8000/docs
- **Alternative API Documentation (ReDoc)**: http://localhost:8000/redoc

---

## How to Run Tests

### Test Suite Overview

The project includes comprehensive test coverage across three test files:

- **`tests/test_models.py`**: Unit tests for database models (EmeraldLot, Counterparty, Trade) including validation, relationships, and constraints
- **`tests/test_crud.py`**: Unit tests for CRUD operations (create, read, update, delete) for all entities, plus inventory and P&L reporting functions
- **`tests/test_api.py`**: Integration tests for FastAPI endpoints, testing HTTP requests and responses

### Running Tests with pytest

```bash
# Run all tests with coverage reporting
pytest tests/ -v --cov=. --cov-report=html --cov-report=term-missing --cov-fail-under=90
```

### Using the Test Script

Alternatively, use the provided test runner:

```bash
python run_tests.py
```

This script:
- Checks dependencies
- Runs all tests with coverage
- Generates HTML coverage reports
- Enforces 90% minimum coverage threshold

### Coverage Requirements

- **Minimum Coverage**: 90% (configured in `pytest.ini`)
- **Coverage Reports**: 
  - HTML report: `htmlcov/index.html`
  - Terminal output: Shows missing lines
- **Coverage Configuration**: Defined in `pytest.ini` with `--cov-fail-under=90`

### Test Configuration

The `pytest.ini` file configures:
- Test discovery: `tests/` directory
- Coverage: All files in project root (`.`)
- Reports: HTML and terminal output
- Minimum threshold: 90% coverage required

---

## Docker Instructions

### Build Docker Image Locally

```bash
# Build the Docker image
docker build -t emerald-ledger:latest .
```

The `Dockerfile`:
- Uses `python:3.12-slim` base image
- Installs dependencies from `requirements.txt`
- Copies application code
- Exposes port 80 for Azure deployment
- Runs uvicorn on `0.0.0.0:80`

### Run Container Locally

```bash
# Run the container, mapping port 80 to host port 8000
docker run -p 8000:80 emerald-ledger:latest
```

**Note**: The container exposes port 80 internally (as required for Azure Web App), but you can map it to any host port (e.g., 8000) for local testing.

Access the application at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs

### Docker Build Context

The `.dockerignore` file excludes:
- Virtual environment (`.venv`)
- Python cache (`__pycache__`)
- Git files (`.git`)
- Coverage reports (`htmlcov`)
- Test database files (`*.db`, except `emerald.db`)
- Test files (`tests/`)

---

## CI Pipeline Explanation

**File**: `.github/workflows/ci.yml`

### Trigger Conditions

The CI pipeline runs on:
- **Push events** to branches: `dev`, `main`, `refactor-code-quality`, `ci-pipeline`, `dockerization`, `deployment`, `monitoring-health`, `docs-report`, `testing`
- **Pull requests** to branches: `dev`, `main`

### Pipeline Steps

1. **Checkout Repository**
   - Uses `actions/checkout@v4` to fetch code

2. **Set up Python**
   - Uses `actions/setup-python@v5`
   - Python version: `3.12`

3. **Cache pip Dependencies**
   - Uses `actions/cache@v4` to cache pip packages
   - Cache key based on `requirements.txt` hash

4. **Install Dependencies**
   - Upgrades pip
   - Installs packages from `requirements.txt`

5. **Run Tests with Coverage**
   - Executes `pytest` on `tests/` directory
   - Generates coverage reports (XML and terminal)
   - **Coverage threshold**: 70% (CI requirement)
   - Verbose output with short traceback format

6. **Build Application**
   - Compiles Python files (`main.py`, `crud.py`, `database.py`, `models.py`, `schemas.py`)
   - Validates imports to ensure no syntax errors

7. **Upload Coverage Reports**
   - Uploads `coverage.xml` and `htmlcov/` as artifacts
   - Retention: 30 days

---

## CD Pipeline Explanation

**File**: `.github/workflows/ci-cd.yaml`

### Trigger Conditions

The CD pipeline runs on:
- **Push events** to `main` branch only
- **Manual workflow dispatch** (manual trigger option)

### Pipeline Steps

1. **Checkout Code**
   - Uses `actions/checkout@v4`

2. **Login to Azure**
   - Uses `azure/login@v2`
   - Authenticates using `AZURE_CREDENTIALS` secret

3. **Build Docker Image**
   - Builds Docker image with tag: `${{ secrets.AZURE_REGISTRY_LOGIN_SERVER }}/emerald-app:latest`

4. **Login to ACR (Azure Container Registry)**
   - Authenticates to ACR using:
     - `AZURE_REGISTRY_LOGIN_SERVER` secret
     - `AZURE_REGISTRY_USERNAME` secret
     - `AZURE_REGISTRY_PASSWORD` secret

5. **Push Image to ACR**
   - Pushes the built image to Azure Container Registry

6. **Deploy to Azure Web App**
   - Uses `azure/webapps-deploy@v2`
   - Deploys the containerized application
   - Uses `AZURE_WEBAPP_NAME` secret to identify the target Web App

### Required Secrets

The CD pipeline requires the following GitHub secrets:
- `AZURE_CREDENTIALS`: Azure service principal credentials
- `AZURE_REGISTRY_LOGIN_SERVER`: ACR login server URL (e.g., `myregistry.azurecr.io`)
- `AZURE_REGISTRY_USERNAME`: ACR username
- `AZURE_REGISTRY_PASSWORD`: ACR password
- `AZURE_WEBAPP_NAME`: Name of the Azure Web App

---

## Monitoring Endpoints

### `/health`

**Purpose**: Simple health check endpoint for Azure Web App health monitoring.

**Method**: `GET`

**Response**:
```json
{
  "status": "healthy",
  "service": "emerald-ledger-api"
}
```

**Use Case**: Azure Web App uses this endpoint to verify the application is running and responsive.

### `/metrics`

**Purpose**: Basic monitoring metrics for application observability.

**Method**: `GET`

**Response**:
```json
{
  "uptime_seconds": 12345.67,
  "total_requests": 42
}
```

**Metrics Explained**:
- `uptime_seconds`: Time elapsed since application startup (in seconds)
- `total_requests`: Total number of HTTP requests processed since startup (tracked via middleware)

**Implementation**: 
- Uptime calculated from `startup_time` (recorded at application startup)
- Request count incremented by `metrics_middleware` on each HTTP request

### Accessing Monitoring Endpoints

Both endpoints are available:
- **Via API**: `GET http://localhost:8000/health` and `GET http://localhost:8000/metrics`
- **Via Swagger UI**: Navigate to http://localhost:8000/docs and expand the `/health` and `/metrics` endpoints
- **Via ReDoc**: Available in the alternative documentation at http://localhost:8000/redoc

---

## Folder Structure

```
Emerald-Devops-IEU/
├── .github/
│   └── workflows/
│       ├── ci.yml              # CI pipeline configuration
│       └── ci-cd.yaml          # CD pipeline configuration
├── frontend/                   # React frontend application
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   │   ├── components/         # React components (modals, tables)
│   │   ├── sections/           # Page sections (Dashboard, Emeralds, Trades, Counterparties)
│   │   ├── api.js              # API client configuration
│   │   ├── App.jsx             # Main React application
│   │   └── index.js            # React entry point
│   ├── package.json
│   └── README.md
├── tests/                      # Test suite
│   ├── conftest.py             # Pytest fixtures and test configuration
│   ├── test_api.py             # API endpoint integration tests
│   ├── test_crud.py            # CRUD operation unit tests
│   └── test_models.py          # Database model unit tests
├── htmlcov/                    # Coverage report HTML files (generated)
├── __pycache__/                # Python bytecode cache
├── .dockerignore               # Docker build exclusions
├── crud.py                     # CRUD operations for all entities
├── database.py                 # Database connection and session management
├── Dockerfile                  # Docker image definition
├── emerald.db                  # SQLite database file
├── main.py                     # FastAPI application and API endpoints
├── models.py                   # SQLAlchemy database models
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
├── run_tests.py                # Test runner script
├── schemas.py                  # Pydantic request/response schemas
└── README.md                   # This file
```

### Key Files

- **`main.py`**: FastAPI application with all API endpoints, CORS middleware, and monitoring endpoints
- **`models.py`**: SQLAlchemy ORM models (EmeraldLot, Counterparty, Trade) with relationships
- **`crud.py`**: Database operations (create, read, update, delete) for all entities
- **`schemas.py`**: Pydantic schemas for request validation and response serialization
- **`database.py`**: Database engine, session factory, and dependency injection for FastAPI
- **`tests/conftest.py`**: Pytest fixtures for test database and test client setup

---

## API Endpoints Summary

### Emeralds
- `POST /emeralds/` - Create emerald lot
- `GET /emeralds/` - List all emeralds (with pagination)
- `GET /emeralds/{emerald_id}` - Get single emerald
- `PUT /emeralds/{emerald_id}` - Update emerald
- `DELETE /emeralds/{emerald_id}` - Delete emerald

### Counterparties
- `POST /counterparties/` - Create counterparty
- `GET /counterparties/` - List all counterparties (with pagination)
- `PUT /counterparties/{cp_id}` - Update counterparty
- `DELETE /counterparties/{cp_id}` - Delete counterparty

### Trades
- `POST /trades/` - Create trade
- `GET /trades/` - List all trades (with pagination)
- `GET /trades/{trade_id}` - Get single trade
- `PUT /trades/{trade_id}` - Update trade
- `DELETE /trades/{trade_id}` - Delete trade

### Reports
- `GET /reports/inventory` - Get current inventory (emeralds with IN_STOCK status)
- `GET /reports/pnl` - Get profit & loss report (total cost, revenue, profit)

### Monitoring
- `GET /health` - Health check endpoint
- `GET /metrics` - Application metrics

---

## Additional Information

- **API Documentation**: Available at http://localhost:8000/docs (Swagger UI) when running locally
- **Database**: SQLite with foreign key constraints enabled for referential integrity
- **CORS**: Configured to allow requests from `http://localhost:3000` (React frontend)
- **Error Handling**: Comprehensive error handling with appropriate HTTP status codes (404, 400, 500)
