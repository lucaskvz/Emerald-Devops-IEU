# Emerald Ledger

## Project Snapshot
- **Name**: Emerald Ledger  
- **Goal**: Record each emerald (or lot), purchase details, sale details, and link to suppliers/buyers.  
- **Stack**: FastAPI (Python) + SQLite + React Frontend.  
- **Why it fits the brief**: CRUD (emeralds, counterparties, trades), persistent DB, REST endpoints + modern UI, UML/architecture, SDLC write-up.  

## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/<your-username>/emerald-ledger.git
cd emerald-ledger
```

### 2. Backend Setup
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate      # Linux/Mac
# .venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Initialize database
python database.py

# Start backend server
uvicorn main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm start
```

## Testing

### Running Tests
```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests with coverage
python run_tests.py

# Or run tests manually
pytest tests/ -v --cov=. --cov-report=html --cov-report=term-missing --cov-fail-under=90
```

### Test Coverage
- **Target**: >90% code coverage
- **Report**: Generated in `htmlcov/index.html`
- **Coverage includes**:
  - Database models and relationships
  - CRUD operations
  - API endpoints
  - Business logic and validation

### Test Structure
```
tests/
├── conftest.py          # Test configuration and fixtures
├── test_models.py       # Database model tests
├── test_crud.py         # CRUD operation tests
└── test_api.py          # API endpoint tests
```

## API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure
```
├── main.py              # FastAPI application
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── crud.py              # Database operations
├── database.py          # Database configuration
├── requirements.txt     # Python dependencies
├── pytest.ini          # Test configuration
├── run_tests.py        # Test runner script
├── tests/              # Test suite
└── frontend/           # React frontend
```

## Development
- **Backend**: FastAPI with SQLAlchemy ORM
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: React with Tailwind CSS
- **Testing**: pytest with coverage reporting
- **Code Quality**: Type hints, docstrings, error handling
