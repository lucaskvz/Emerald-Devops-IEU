# Emerald Ledger

## Project Overview

**Name:** Emerald Ledger  
**Description:** A comprehensive gemstone trading management system for tracking emerald inventory, counterparty relationships, and financial transactions.

**Purpose:** This system enables gemstone traders to maintain detailed records of emerald lots, manage supplier and buyer relationships, track all trading transactions, and generate financial reports for business analysis.

**Assignment Fit:** The project fulfills all core requirements:
- **CRUD Operations:** Complete Create, Read, Update, Delete functionality for all entities
- **Persistent Storage:** SQLite database with SQLAlchemy ORM for data persistence
- **REST API:** FastAPI backend with comprehensive endpoint coverage
- **Optional UI:** React frontend providing intuitive user interface
- **Business Logic:** Complex relationships, financial calculations, and reporting

**Technologies Used:**
- **Backend:** FastAPI, SQLAlchemy, Pydantic, SQLite
- **Frontend:** React, Axios, CSS3
- **Testing:** pytest, coverage reporting
- **Development:** Python 3.13, Node.js, npm

## Setup Instructions

### Prerequisites
- Python 3.11+ (recommended for compatibility)
- Node.js 16+
- npm or yarn

### Backend Setup
```bash
# Clone repository
git clone <repository-url>
cd Emerald-Devops-IEU

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Initialize database
python database.py

# Start backend server
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Access Points
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs (Swagger UI)
- **Frontend:** http://localhost:3000

## Features

### Core CRUD Operations
- **Emerald Lots:** Track individual gems with gemological properties (carat, shape, color, clarity, origin, certificate)
- **Counterparties:** Manage suppliers, buyers, and brokers with contact information and KYC notes
- **Trades:** Record all transactions with financial details, dates, and relationships

### Advanced Features
- **Inventory Management:** Real-time stock tracking with status updates
- **Financial Reporting:** Automated P&L calculations and profit analysis
- **Relationship Mapping:** Complex foreign key relationships between entities
- **Data Validation:** Comprehensive input validation and error handling
- **Partial Updates:** Support for incremental data modifications

### Business Intelligence
- **Auto-computed Metrics:** ROI calculations, holding periods, profit margins
- **Inventory Reports:** Current stock levels and status tracking
- **Financial Analytics:** Revenue, cost, and profit analysis
- **Transaction History:** Complete audit trail of all trading activities

## Testing

### Test Coverage
- **Comprehensive Test Suite:** 55+ unit tests covering all functionality
- **Coverage Requirement:** >90% code coverage (currently 93.04%)
- **Test Categories:**
  - Model validation and relationships
  - CRUD operations with edge cases
  - API endpoint functionality
  - Error handling and business logic

### Running Tests
```bash
# Run all tests with coverage
python run_tests.py

# Manual test execution
pytest tests/ -v --cov=. --cov-report=html --cov-report=term-missing --cov-fail-under=90
```

### Test Reports
- **HTML Coverage Report:** Generated in `htmlcov/index.html`
- **Terminal Output:** Detailed coverage analysis with missing lines
- **Quality Metrics:** Test success rates and coverage statistics

## Architecture Overview

### System Flow
```
React Frontend ↔ FastAPI Backend ↔ SQLAlchemy ORM ↔ SQLite Database
     ↓              ↓                    ↓              ↓
  UI Components   REST Endpoints    Data Models    Persistent Storage
  State Management  Validation      Relationships   Transaction Logs
  API Integration  Error Handling  Business Logic  Data Integrity
```

### Component Architecture
- **Frontend:** React components with centralized API client
- **Backend:** FastAPI with dependency injection and middleware
- **Database:** SQLAlchemy ORM with proper relationships and constraints
- **Testing:** Isolated test database with comprehensive fixtures

### Data Flow
1. **User Interaction:** Frontend components capture user input
2. **API Communication:** Axios client sends HTTP requests to FastAPI
3. **Request Processing:** FastAPI validates input via Pydantic schemas
4. **Business Logic:** CRUD operations execute with SQLAlchemy
5. **Data Persistence:** SQLite stores data with referential integrity
6. **Response Generation:** Serialized data returned to frontend
7. **UI Updates:** React components re-render with new data

## SDLC Model

### Agile Iterative Development
This project followed an **Agile Iterative** development model with the following phases:

#### Phase 1: Foundation
- Database schema design and model creation
- Basic CRUD operations implementation
- API endpoint development

#### Phase 2: Business Logic
- Trade relationship management
- Financial calculation implementation
- Reporting functionality

#### Phase 3: User Interface
- React frontend development
- Component architecture and state management
- API integration and error handling

#### Phase 4: Quality Assurance
- Comprehensive testing suite development
- Coverage analysis and optimization
- Code quality improvements and refactoring

#### Phase 5: Documentation & Deployment
- README and technical documentation
- Deployment preparation and optimization
- Final testing and validation

## Reflection / DevOps Scaling

### Current State
- **Development Environment:** Local development with SQLite
- **Testing:** Comprehensive unit test coverage
- **Documentation:** Complete API documentation with Swagger

### Future Scaling Opportunities
- **Containerization:** Docker containers for consistent deployment
- **Database Migration:** PostgreSQL for production scalability
- **CI/CD Pipeline:** Automated testing and deployment
- **Cloud Deployment:** AWS/Azure/GCP integration
- **Monitoring:** Application performance monitoring and logging
- **Security:** Authentication, authorization, and data encryption
- **Microservices:** Service decomposition for scalability

### DevOps Considerations
- **Infrastructure as Code:** Terraform for cloud resources
- **Container Orchestration:** Kubernetes for production deployment
- **Monitoring:** Prometheus/Grafana for system observability
- **Security:** OWASP compliance and vulnerability scanning

## Credits / AI Disclosure

This project was developed with AI assistance to accelerate development and ensure best practices. The AI was used for:
- Code generation and optimization
- Architecture design and implementation
- Testing strategy and coverage analysis
- Documentation and technical writing

**AI Prompts and detailed usage are documented in the project appendices** to maintain transparency and provide context for the development process.

## Repository Information

### Commit History
- **Meaningful Commits:** Each commit represents a logical development step
- **Clear Messages:** Descriptive commit messages following conventional format
- **Incremental Development:** Small, focused changes for better tracking

### File Structure
```
├── Backend (Python/FastAPI)
│   ├── Core Application Files
│   ├── Database Models & Schemas
│   ├── CRUD Operations
│   └── Comprehensive Test Suite
├── Frontend (React)
│   ├── Component Architecture
│   ├── API Integration
│   └── User Interface
└── Documentation
    ├── README
    ├── API Documentation
    └── Development Notes
```

### Code Quality
- **Clean Architecture:** Separation of concerns with clear boundaries
- **Type Safety:** Pydantic schemas and TypeScript-like patterns
- **Error Handling:** Comprehensive exception management
- **Performance:** Optimized queries and efficient data structures
- **Maintainability:** Well-documented code with clear naming conventions

---

**Repository:** [https://github.com/lucaskvz/Emerald-Devops-IEU.git]  
**Documentation:** Available in `/docs` directory  
**API Reference:** http://localhost:8000/docs  
**Test Coverage:** Available in `/htmlcov` directory
