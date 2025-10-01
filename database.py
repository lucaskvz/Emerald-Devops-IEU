# database.py
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "sqlite:///./emerald.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Enable SQLite foreign key constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """I enable foreign key constraints on SQLite connections to enforce referential integrity."""
    try:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    except Exception:
        pass  # ignore for non-sqlite drivers

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI routes
def get_db():
    """I provide database sessions to FastAPI routes with automatic cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Always create tables when imported
Base.metadata.create_all(bind=engine)