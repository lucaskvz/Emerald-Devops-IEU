# schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum

# --- Enums (match models.py) ---
class LotStatus(str, Enum):
    IN_STOCK = "IN_STOCK"
    SOLD = "SOLD"

class CounterpartyType(str, Enum):
    SUPPLIER = "SUPPLIER"
    BUYER = "BUYER"
    BOTH = "BOTH"

class TradeType(str, Enum):
    PURCHASE = "PURCHASE"
    SALE = "SALE"

# --- EmeraldLot ---
class EmeraldLotBase(BaseModel):
    lot_code: str
    carat: float
    shape: Optional[str] = None
    color_grade: Optional[str] = None
    clarity: Optional[str] = None
    treatment: Optional[str] = None
    origin: Optional[str] = None
    certificate_id: Optional[str] = None
    notes: Optional[str] = None
    status: LotStatus = LotStatus.IN_STOCK

class EmeraldLotCreate(EmeraldLotBase):
    pass

class EmeraldLotRead(EmeraldLotBase):
    id: int
    class Config:
        from_attributes = True

# --- Counterparty ---
class CounterpartyBase(BaseModel):
    name: str
    type: CounterpartyType
    contact_info: Optional[str] = None
    country: Optional[str] = None
    kyc_notes: Optional[str] = None

class CounterpartyCreate(CounterpartyBase):
    pass

class CounterpartyRead(CounterpartyBase):
    id: int
    class Config:
        orm_mode = True

# --- Trade ---
class TradeBase(BaseModel):
    type: TradeType
    date: date
    currency: str
    unit_price: float
    total_price: float
    location: Optional[str] = None
    emerald_lot_id: int
    counterparty_id: int

class TradeCreate(TradeBase):
    pass

class TradeRead(TradeBase):
    id: int
    class Config:
        orm_mode = True
