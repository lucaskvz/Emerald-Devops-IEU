from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()

# --- Enums ---
class LotStatus(str, enum.Enum):
    IN_STOCK = "IN_STOCK"
    SOLD = "SOLD"

class CounterpartyType(str, enum.Enum):
    SUPPLIER = "SUPPLIER"
    BUYER = "BUYER"
    BOTH = "BOTH"

class TradeType(str, enum.Enum):
    PURCHASE = "PURCHASE"
    SALE = "SALE"

# --- Models ---
class EmeraldLot(Base):
    __tablename__ = "emerald_lots"

    id = Column(Integer, primary_key=True, index=True)
    lot_code = Column(String, unique=True, index=True, nullable=False)
    carat = Column(Float, nullable=False)
    shape = Column(String)
    color_grade = Column(String)
    clarity = Column(String)
    treatment = Column(String)
    origin = Column(String)
    certificate_id = Column(String, nullable=True)
    status = Column(Enum(LotStatus), default=LotStatus.IN_STOCK)

    # Relationships
    trades = relationship("Trade", back_populates="emerald_lot")


class Counterparty(Base):
    __tablename__ = "counterparties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    type = Column(Enum(CounterpartyType), nullable=False)
    contact_info = Column(String, nullable=True)
    country = Column(String, nullable=True)
    kyc_notes = Column(Text, nullable=True)

    # Relationships
    trades = relationship("Trade", back_populates="counterparty")


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(TradeType), nullable=False)  # PURCHASE or SALE
    date = Column(Date, nullable=False)
    currency = Column(String, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    location = Column(String, nullable=True)

    # Foreign keys
    emerald_lot_id = Column(Integer, ForeignKey("emerald_lots.id"))
    counterparty_id = Column(Integer, ForeignKey("counterparties.id"))

    # Relationships
    emerald_lot = relationship("EmeraldLot", back_populates="trades")
    counterparty = relationship("Counterparty", back_populates="trades")
