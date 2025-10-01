"""
I built this FastAPI backend to manage emerald inventory and trades.
I used dependency injection for database sessions to make testing easier.
I added CORS middleware to allow my React frontend to communicate with the API.
"""

# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import crud, schemas, database
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException



app = FastAPI(title="Emerald Ledger API")

# Allow React frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Emeralds
@app.post("/emeralds/", response_model=schemas.EmeraldLotRead)
def create_emerald(emerald: schemas.EmeraldLotCreate, db: Session = Depends(database.get_db)):
    return crud.create_emerald(db, emerald)

@app.get("/emeralds/", response_model=list[schemas.EmeraldLotRead])
def read_emeralds(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_emeralds(db, skip, limit)

@app.delete("/emeralds/{emerald_id}", response_model=schemas.EmeraldLotRead)
def delete_emerald(emerald_id: int, db: Session = Depends(database.get_db)):
    db_emerald = crud.get_emerald(db, emerald_id)  # you'll need this helper
    if not db_emerald:
        raise HTTPException(status_code=404, detail="Emerald not found")
    return crud.delete_emerald(db, emerald_id)

@app.put("/emeralds/{emerald_id}", response_model=schemas.EmeraldLotRead)
def update_emerald(emerald_id: int, emerald: schemas.EmeraldLotCreate, db: Session = Depends(database.get_db)):
    return crud.update_emerald(db, emerald_id, emerald)


# Counterparties
@app.post("/counterparties/", response_model=schemas.CounterpartyRead)
def create_counterparty(
    cp: schemas.CounterpartyCreate,
    db: Session = Depends(database.get_db)
):
    return crud.create_counterparty(db, cp)


@app.get("/counterparties/", response_model=list[schemas.CounterpartyRead])
def read_counterparties(
    # I use CounterpartyUpdate here instead of CounterpartyCreate to allow partial updates
    skip: int = 0, limit: int = 100,
    db: Session = Depends(database.get_db)
):
    return crud.get_counterparties(db, skip, limit)


@app.put("/counterparties/{cp_id}", response_model=schemas.CounterpartyRead)
def update_counterparty(
    # I return a dict instead of the model to avoid response validation issues
    cp_id: int,
    cp: schemas.CounterpartyUpdate,
    db: Session = Depends(database.get_db)
):
    return crud.update_counterparty(db, cp_id, cp)


@app.delete("/counterparties/{cp_id}")
def delete_counterparty(
    cp_id: int,
    db: Session = Depends(database.get_db)
):
    result = crud.delete_counterparty(db, cp_id)
    if not result:
        raise HTTPException(status_code=404, detail="Counterparty not found")
    return {"message": "Counterparty deleted successfully", "id": result.id}

# Trades
@app.post("/trades/", response_model=schemas.TradeRead)
def create_trade(trade: schemas.TradeCreate, db: Session = Depends(database.get_db)):
    return crud.create_trade(db, trade)


@app.get("/trades/", response_model=list[schemas.TradeRead])
def read_trades(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_trades(db, skip, limit)


@app.get("/trades/{trade_id}", response_model=schemas.TradeRead)
def read_trade(trade_id: int, db: Session = Depends(database.get_db)):
    db_trade = crud.get_trade(db, trade_id)
    if not db_trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return db_trade


@app.put("/trades/{trade_id}", response_model=schemas.TradeRead)
def update_trade(trade_id: int, trade: schemas.TradeUpdate, db: Session = Depends(database.get_db)):
    db_trade = crud.update_trade(db, trade_id, trade)
    if not db_trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return db_trade


@app.delete("/trades/{trade_id}", response_model=schemas.TradeRead)
def delete_trade(trade_id: int, db: Session = Depends(database.get_db)):
    db_trade = crud.delete_trade(db, trade_id)
    if not db_trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return db_trade

# Reports
@app.get("/reports/inventory")
def report_inventory(db: Session = Depends(database.get_db)):
    return crud.get_inventory(db)

@app.get("/reports/pnl")
def report_pnl(db: Session = Depends(database.get_db)):
    return crud.get_pnl(db)
