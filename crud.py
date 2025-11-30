"""
I implemented all CRUD operations using SQLAlchemy ORM.
I use model_dump() instead of dict() for Pydantic v2 compatibility.
I return None for not-found cases to let the API layer handle 404 responses.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import EmeraldLot, Counterparty, Trade, LotStatus, TradeType
import schemas

# Constants
DEFAULT_SKIP = 0
DEFAULT_LIMIT = 100

# Helper functions
def _create_entity(db: Session, model_class, schema_data):
    """Helper to create and persist a new entity."""
    db_obj = model_class(**schema_data.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def _update_entity_fields(db_obj, update_data):
    """Helper to update entity fields from a dictionary."""
    for key, value in update_data.items():
        setattr(db_obj, key, value)


def _commit_and_refresh(db: Session, db_obj):
    """Helper to commit changes and refresh the object."""
    db.commit()
    db.refresh(db_obj)
    return db_obj


def _delete_entity(db: Session, db_obj):
    """Helper to delete an entity with error handling."""
    if db_obj:
        try:
            db.delete(db_obj)
            db.commit()
            return db_obj
        except IntegrityError as e:
            db.rollback()
            raise ValueError("Cannot delete: this entity has associated records that prevent deletion") from e
        except Exception as e:
            db.rollback()
            raise
    return None


# --- EmeraldLot ---
def create_emerald(db: Session, emerald: schemas.EmeraldLotCreate):
    return _create_entity(db, EmeraldLot, emerald)


def get_emeralds(db: Session, skip: int = DEFAULT_SKIP, limit: int = DEFAULT_LIMIT):
    return db.query(EmeraldLot).offset(skip).limit(limit).all()


def get_emerald(db: Session, emerald_id: int):
    """Fetch a single emerald by ID."""
    return db.query(EmeraldLot).filter(EmeraldLot.id == emerald_id).first()


def update_emerald(db: Session, emerald_id: int, emerald: schemas.EmeraldLotCreate):
    db_obj = get_emerald(db, emerald_id)
    if not db_obj:
        return None
    _update_entity_fields(db_obj, emerald.model_dump())
    return _commit_and_refresh(db, db_obj)


def delete_emerald(db: Session, emerald_id: int):
    emerald = get_emerald(db, emerald_id)
    return _delete_entity(db, emerald)


# --- Counterparty ---
def create_counterparty(db: Session, cp: schemas.CounterpartyCreate):
    return _create_entity(db, Counterparty, cp)


def get_counterparties(db: Session, skip: int = DEFAULT_SKIP, limit: int = DEFAULT_LIMIT):
    return db.query(Counterparty).offset(skip).limit(limit).all()


def get_counterparty(db: Session, cp_id: int):
    return db.query(Counterparty).filter(Counterparty.id == cp_id).first()


def update_counterparty(db: Session, cp_id: int, cp: schemas.CounterpartyUpdate):
    db_cp = get_counterparty(db, cp_id)
    if not db_cp:
        return None
    update_data = cp.model_dump(exclude_unset=True)
    _update_entity_fields(db_cp, update_data)
    return _commit_and_refresh(db, db_cp)


def delete_counterparty(db: Session, cp_id: int):
    """Delete a counterparty, checking for associated trades first."""
    db_cp = get_counterparty(db, cp_id)
    if not db_cp:
        return None
    
    # Check if counterparty has associated trades
    trade_count = db.query(Trade).filter(Trade.counterparty_id == cp_id).count()
    if trade_count > 0:
        raise ValueError(
            f"Cannot delete counterparty: {trade_count} trade(s) are associated with this counterparty. "
            "Please delete or reassign the trades first."
        )
    
    return _delete_entity(db, db_cp)


# --- Trade ---
def create_trade(db: Session, trade: schemas.TradeCreate):
    return _create_entity(db, Trade, trade)


def get_trades(db: Session, skip: int = DEFAULT_SKIP, limit: int = DEFAULT_LIMIT):
    return db.query(Trade).offset(skip).limit(limit).all()


def get_trade(db: Session, trade_id: int):
    return db.query(Trade).filter(Trade.id == trade_id).first()


def update_trade(db: Session, trade_id: int, trade: schemas.TradeUpdate):
    db_trade = get_trade(db, trade_id)
    if not db_trade:
        return None
    update_data = trade.model_dump(exclude_unset=True)
    _update_entity_fields(db_trade, update_data)
    return _commit_and_refresh(db, db_trade)


def delete_trade(db: Session, trade_id: int):
    db_trade = get_trade(db, trade_id)
    return _delete_entity(db, db_trade)


# --- Reports ---
def get_inventory(db: Session):
    """Return emerald lots currently in stock."""
    return db.query(EmeraldLot).filter(EmeraldLot.status == LotStatus.IN_STOCK).all()


def _calculate_total_price(trades):
    """Helper to calculate total price from a list of trades."""
    return sum(t.total_price for t in trades)


def get_pnl(db: Session):
    """Compute total cost, revenue, and profit from trades."""
    purchases = db.query(Trade).filter(Trade.type == TradeType.PURCHASE).all()
    sales = db.query(Trade).filter(Trade.type == TradeType.SALE).all()

    total_cost = _calculate_total_price(purchases)
    total_revenue = _calculate_total_price(sales)

    return {
        "total_cost": total_cost,
        "total_revenue": total_revenue,
        "profit": total_revenue - total_cost,
    }