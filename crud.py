from sqlalchemy.orm import Session
from models import EmeraldLot, Counterparty, Trade
import schemas

# --- EmeraldLot ---
def create_emerald(db: Session, emerald: schemas.EmeraldLotCreate):
    db_emerald = EmeraldLot(**emerald.dict())
    db.add(db_emerald)
    db.commit()
    db.refresh(db_emerald)
    return db_emerald


def get_emeralds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(EmeraldLot).offset(skip).limit(limit).all()


def get_emerald(db: Session, emerald_id: int):
    """Fetch a single emerald by ID."""
    return db.query(EmeraldLot).filter(EmeraldLot.id == emerald_id).first()


def update_emerald(db: Session, emerald_id: int, emerald: schemas.EmeraldLotCreate):
    db_obj = get_emerald(db, emerald_id)
    if not db_obj:
        return None
    for field, value in emerald.dict().items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_emerald(db: Session, emerald_id: int):
    emerald = get_emerald(db, emerald_id)
    if emerald:
        db.delete(emerald)
        db.commit()
        return emerald
    return None


# --- Counterparty ---
def create_counterparty(db: Session, cp: schemas.CounterpartyCreate):
    db_cp = Counterparty(**cp.dict())
    db.add(db_cp)
    db.commit()
    db.refresh(db_cp)
    return db_cp


def get_counterparties(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Counterparty).offset(skip).limit(limit).all()


def get_counterparty(db: Session, cp_id: int):
    return db.query(Counterparty).filter(Counterparty.id == cp_id).first()


def update_counterparty(db: Session, cp_id: int, cp: schemas.CounterpartyUpdate):
    db_cp = get_counterparty(db, cp_id)
    if not db_cp:
        return None
    update_data = cp.dict(exclude_unset=True)  # ✅ allow partial updates
    for key, value in update_data.items():
        setattr(db_cp, key, value)
    db.commit()
    db.refresh(db_cp)
    return db_cp


def delete_counterparty(db: Session, cp_id: int):
    db_cp = get_counterparty(db, cp_id)
    if not db_cp:
        return None
    db.delete(db_cp)
    db.commit()
    return db_cp


# --- Trade ---
def create_trade(db: Session, trade: schemas.TradeCreate):
    db_trade = Trade(**trade.dict())
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade


def get_trades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Trade).offset(skip).limit(limit).all()


def get_trade(db: Session, trade_id: int):
    return db.query(Trade).filter(Trade.id == trade_id).first()


def update_trade(db: Session, trade_id: int, trade: schemas.TradeUpdate):
    db_trade = get_trade(db, trade_id)
    if not db_trade:
        return None
    update_data = trade.dict(exclude_unset=True)  # ✅ supports partial updates
    for key, value in update_data.items():
        setattr(db_trade, key, value)
    db.commit()
    db.refresh(db_trade)
    return db_trade


def delete_trade(db: Session, trade_id: int):
    db_trade = get_trade(db, trade_id)
    if not db_trade:
        return None
    db.delete(db_trade)
    db.commit()
    return db_trade


# --- Reports ---
def get_inventory(db: Session):
    """Return emerald lots currently in stock."""
    return db.query(EmeraldLot).filter(EmeraldLot.status == "IN_STOCK").all()


def get_pnl(db: Session):
    """Compute total cost, revenue, and profit from trades."""
    purchases = db.query(Trade).filter(Trade.type == "PURCHASE").all()
    sales = db.query(Trade).filter(Trade.type == "SALE").all()

    total_cost = sum(t.total_price for t in purchases)
    total_revenue = sum(t.total_price for t in sales)

    return {
        "total_cost": total_cost,
        "total_revenue": total_revenue,
        "profit": total_revenue - total_cost,
    }
