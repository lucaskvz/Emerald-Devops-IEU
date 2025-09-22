# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import crud, schemas, database

app = FastAPI(title="Emerald Ledger API")

# Emeralds
@app.post("/emeralds/", response_model=schemas.EmeraldLotRead)
def create_emerald(emerald: schemas.EmeraldLotCreate, db: Session = Depends(database.get_db)):
    return crud.create_emerald(db, emerald)

@app.get("/emeralds/", response_model=list[schemas.EmeraldLotRead])
def read_emeralds(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_emeralds(db, skip, limit)

# Counterparties
@app.post("/counterparties/", response_model=schemas.CounterpartyRead)
def create_counterparty(cp: schemas.CounterpartyCreate, db: Session = Depends(database.get_db)):
    return crud.create_counterparty(db, cp)

@app.get("/counterparties/", response_model=list[schemas.CounterpartyRead])
def read_counterparties(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_counterparties(db, skip, limit)

# Trades
@app.post("/trades/", response_model=schemas.TradeRead)
def create_trade(trade: schemas.TradeCreate, db: Session = Depends(database.get_db)):
    return crud.create_trade(db, trade)

@app.get("/trades/", response_model=list[schemas.TradeRead])
def read_trades(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_trades(db, skip, limit)

# Reports
@app.get("/reports/inventory")
def report_inventory(db: Session = Depends(database.get_db)):
    return crud.get_inventory(db)

@app.get("/reports/pnl")
def report_pnl(db: Session = Depends(database.get_db)):
    return crud.get_pnl(db)
