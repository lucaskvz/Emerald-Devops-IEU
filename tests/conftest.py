"""
I configure test fixtures here to avoid code duplication across test files.
I use an in-memory SQLite database that gets recreated for each test.
I override the database dependency to inject the test database.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import get_db, Base
from models import EmeraldLot, Counterparty, Trade, LotStatus, CounterpartyType, TradeType
from schemas import EmeraldLotCreate, CounterpartyCreate, TradeCreate
from datetime import date


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database dependency override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_emerald_data():
    """Sample emerald data for testing."""
    return {
        "lot_code": "EM001",
        "carat": 2.5,
        "shape": "Round",
        "color_grade": "G",
        "clarity": "VS1",
        "treatment": "None",
        "origin": "Colombia",
        "certificate_id": "GIA123456",
        "status": LotStatus.IN_STOCK
    }


@pytest.fixture
def sample_counterparty_data():
    """Sample counterparty data for testing."""
    return {
        "name": "Test Supplier",
        "type": CounterpartyType.SUPPLIER,
        "contact_info": "test@example.com",
        "country": "Colombia",
        "kyc_notes": "Verified supplier"
    }


@pytest.fixture
def sample_trade_data():
    """Sample trade data for testing."""
    return {
        "type": TradeType.PURCHASE,
        "date": date(2024, 1, 15),
        "currency": "USD",
        "unit_price": 1000.0,
        "total_price": 2500.0,
        "location": "New York",
        "emerald_lot_id": 1,
        "counterparty_id": 1
    }


@pytest.fixture
def sample_emerald(db_session, sample_emerald_data):
    """Create a sample emerald in the database."""
    emerald = EmeraldLot(**sample_emerald_data)
    db_session.add(emerald)
    db_session.commit()
    db_session.refresh(emerald)
    return emerald


@pytest.fixture
def sample_counterparty(db_session, sample_counterparty_data):
    """Create a sample counterparty in the database."""
    counterparty = Counterparty(**sample_counterparty_data)
    db_session.add(counterparty)
    db_session.commit()
    db_session.refresh(counterparty)
    return counterparty


@pytest.fixture
def sample_trade(db_session, sample_trade_data, sample_emerald, sample_counterparty):
    """Create a sample trade in the database."""
    trade_data = sample_trade_data.copy()
    trade_data["emerald_lot_id"] = sample_emerald.id
    trade_data["counterparty_id"] = sample_counterparty.id
    
    trade = Trade(**trade_data)
    db_session.add(trade)
    db_session.commit()
    db_session.refresh(trade)
    return trade
