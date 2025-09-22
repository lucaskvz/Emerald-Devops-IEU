# crud.py
from sqlalchemy.orm import Session
from models import EmeraldLot, Counterparty, Trade
import schemas
from datetime import date

# --- EmeraldLot ---
def create_emerald(db: Session, emerald: schemas.EmeraldLotCreate):
    db_emerald = EmeraldLot(**emerald.dict())
    db.add(db_emerald)
    db.commit()
    db.refresh(db_emerald)
    return db_emerald

def get_emeralds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(EmeraldLot).offset(skip).limit(limit).all()

# --- Counterparty ---
def create_counterparty(db: Session, cp: schemas.CounterpartyCreate):
    db_cp = Counterparty(**cp.dict())
    db.add(db_cp)
    db.commit()
    db.refresh(db_cp)
    return db_cp

def get_counterparties(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Counterparty).offset(skip).limit(limit).all()

# --- Trade ---
def create_trade(db: Session, trade: schemas.TradeCreate):
    db_trade = Trade(**trade.dict())
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade

def get_trades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Trade).offset(skip).limit(limit).all()

# --- Reports ---
def get_inventory(db: Session):
    return db.query(EmeraldLot).filter(EmeraldLot.status == "IN_STOCK").all()

def get_pnl(db: Session):
    # Sum revenues - costs
    total_cost = db.query(Trade).filter(Trade.type == "PURCHASE").with_entities(
        (Trade.total_price).label("total_cost")
    )
    total_revenue = db.query(Trade).filter(Trade.type == "SALE").with_entities(
        (Trade.total_price).label("total_revenue")
    )
    return {
        "total_cost": sum([c.total_cost for c in total_cost]),
        "total_revenue": sum([r.total_revenue for r in total_revenue]),
        "profit": sum([r.total_revenue for r in total_revenue]) - sum([c.total_cost for c in total_cost]),
    }
