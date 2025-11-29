"""
I built this FastAPI backend to manage emerald inventory and trades.
I used dependency injection for database sessions to make testing easier.
I added CORS middleware to allow my React frontend to communicate with the API.
"""

# main.py
from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
import crud, schemas, database
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
import time

# Constants
CORS_ORIGIN = "http://localhost:3000"
ERROR_EMERALD_NOT_FOUND = "Emerald not found"
ERROR_COUNTERPARTY_NOT_FOUND = "Counterparty not found"
ERROR_TRADE_NOT_FOUND = "Trade not found"
SUCCESS_COUNTERPARTY_DELETED = "Counterparty deleted successfully"

app = FastAPI(title="Emerald Ledger API")

# Allow React frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[CORS_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------
# MONITORING + HEALTH CHECK SECTION
# ---------------------------------------

startup_time = time.time()
request_count = 0
error_count = 0
total_latency_seconds = 0.0


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """
    Middleware tracking:
    - total requests
    - total errors (4xx, 5xx, exceptions)
    - total latency
    """
    global request_count, error_count, total_latency_seconds

    start_time = time.perf_counter()
    request_count += 1

    try:
        response = await call_next(request)
    except Exception:
        # Track unhandled exceptions as errors
        error_count += 1
        raise

    # Time spent processing the request
    latency = time.perf_counter() - start_time
    total_latency_seconds += latency

    # Count HTTP 4xx and 5xx responses
    if response.status_code >= 400:
        error_count += 1

    return response


@app.get("/health")
def health():
    """Simple Azure health check endpoint."""
    return {"status": "healthy", "service": "emerald-ledger-api"}


@app.get("/metrics")
def metrics():
    """Monitoring metrics required for assignment (requests, errors, latency, uptime)."""
    uptime_seconds = time.time() - startup_time

    avg_latency_ms = (
        (total_latency_seconds / request_count) * 1000
        if request_count > 0 else 0
    )

    return {
        "uptime_seconds": uptime_seconds,
        "total_requests": request_count,
        "total_errors": error_count,
        "average_latency_ms": avg_latency_ms,
    }

# ---------------------------------------
# END MONITORING SECTION
# ---------------------------------------


def _raise_not_found(entity_name: str):
    """Helper to raise 404 HTTPException for not found entities."""
    error_messages = {
        "Emerald": ERROR_EMERALD_NOT_FOUND,
        "Counterparty": ERROR_COUNTERPARTY_NOT_FOUND,
        "Trade": ERROR_TRADE_NOT_FOUND,
    }
    raise HTTPException(status_code=404, detail=error_messages.get(entity_name, "Not found"))


# Emeralds
@app.post("/emeralds/", response_model=schemas.EmeraldLotRead)
def create_emerald(emerald: schemas.EmeraldLotCreate, db: Session = Depends(database.get_db)):
    return crud.create_emerald(db, emerald)


@app.get("/emeralds/", response_model=list[schemas.EmeraldLotRead])
def read_emeralds(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_emeralds(db, skip, limit)


@app.delete("/emeralds/{emerald_id}", response_model=schemas.EmeraldLotRead)
def delete_emerald(emerald_id: int, db: Session = Depends(database.get_db)):
    db_emerald = crud.get_emerald(db, emerald_id)
    if not db_emerald:
        _raise_not_found("Emerald")
    return crud.delete_emerald(db, emerald_id)


@app.put("/emeralds/{emerald_id}", response_model=schemas.EmeraldLotRead)
def update_emerald(emerald_id: int, emerald: schemas.EmeraldLotCreate, db: Session = Depends(database.get_db)):
    return crud.update_emerald(db, emerald_id, emerald)


# Counterparties
@app.post("/counterparties/", response_model=schemas.CounterpartyRead)
def create_counterparty(cp: schemas.CounterpartyCreate, db: Session = Depends(database.get_db)):
    return crud.create_counterparty(db, cp)


@app.get("/counterparties/", response_model=list[schemas.CounterpartyRead])
def read_counterparties(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_counterparties(db, skip, limit)


@app.put("/counterparties/{cp_id}", response_model=schemas.CounterpartyRead)
def update_counterparty(cp_id: int, cp: schemas.CounterpartyUpdate, db: Session = Depends(database.get_db)):
    return crud.update_counterparty(db, cp_id, cp)


@app.delete("/counterparties/{cp_id}")
def delete_counterparty(cp_id: int, db: Session = Depends(database.get_db)):
    try:
        result = crud.delete_counterparty(db, cp_id)
        if not result:
            _raise_not_found("Counterparty")
        return {"message": SUCCESS_COUNTERPARTY_DELETED, "id": result.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete counterparty: {str(e)}")


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
        _raise_not_found("Trade")
    return db_trade


@app.put("/trades/{trade_id}", response_model=schemas.TradeRead)
def update_trade(trade_id: int, trade: schemas.TradeUpdate, db: Session = Depends(database.get_db)):
    db_trade = crud.update_trade(db, trade_id, trade)
    if not db_trade:
        _raise_not_found("Trade")
    return db_trade


@app.delete("/trades/{trade_id}", response_model=schemas.TradeRead)
def delete_trade(trade_id: int, db: Session = Depends(database.get_db)):
    db_trade = crud.delete_trade(db, trade_id)
    if not db_trade:
        _raise_not_found("Trade")
    return db_trade


# Reports
@app.get("/reports/inventory")
def report_inventory(db: Session = Depends(database.get_db)):
    return crud.get_inventory(db)


@app.get("/reports/pnl")
def report_pnl(db: Session = Depends(database.get_db)):
    return crud.get_pnl(db)
