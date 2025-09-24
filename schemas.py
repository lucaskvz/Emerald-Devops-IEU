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
    status: LotStatus = LotStatus.IN_STOCK

class EmeraldLotCreate(EmeraldLotBase):
    pass

class EmeraldLotRead(EmeraldLotBase):
    id: int
    class Config:
        orm_mode = True  # changed to orm_mode for consistency


# --- Counterparty ---
class CounterpartyBase(BaseModel):
    name: str
    type: CounterpartyType
    contact_info: Optional[str] = None
    country: Optional[str] = None


class CounterpartyCreate(CounterpartyBase):
    pass


class CounterpartyUpdate(BaseModel):  # new schema for updates
    name: Optional[str] = None
    type: Optional[CounterpartyType] = None
    contact_info: Optional[str] = None
    country: Optional[str] = None


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


class TradeUpdate(BaseModel):  # allow partial updates
    type: Optional[TradeType] = None
    date: Optional[date] = None
    currency: Optional[str] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None
    location: Optional[str] = None
    emerald_lot_id: Optional[int] = None
    counterparty_id: Optional[int] = None


class TradeRead(TradeBase):
    id: int
    roi: Optional[float] = None
    holding_days: Optional[int] = None

    class Config:
        orm_mode = True
