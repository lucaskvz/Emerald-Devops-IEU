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
    skip: int = 0, limit: int = 100,
    db: Session = Depends(database.get_db)
):
    return crud.get_counterparties(db, skip, limit)


@app.put("/counterparties/{cp_id}", response_model=schemas.CounterpartyRead)
def update_counterparty(
    cp_id: int,
    cp: schemas.CounterpartyCreate,
    db: Session = Depends(database.get_db)
):
    return crud.update_counterparty(db, cp_id, cp)


@app.delete("/counterparties/{cp_id}", response_model=dict)
def delete_counterparty(
    cp_id: int,
    db: Session = Depends(database.get_db)
):
    return crud.delete_counterparty(db, cp_id)

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
