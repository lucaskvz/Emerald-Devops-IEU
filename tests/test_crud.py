"""
Unit tests for CRUD operations.
"""
import pytest
from datetime import date
from crud import (
    create_emerald, get_emeralds, get_emerald, update_emerald, delete_emerald,
    create_counterparty, get_counterparties, get_counterparty, update_counterparty, delete_counterparty,
    create_trade, get_trades, get_trade, update_trade, delete_trade,
    get_inventory, get_pnl
)
from schemas import EmeraldLotCreate, CounterpartyCreate, CounterpartyUpdate, TradeCreate, TradeUpdate
from models import LotStatus, CounterpartyType, TradeType


class TestEmeraldCRUD:
    """Test emerald CRUD operations."""
    
    def test_create_emerald(self, db_session):
        """Test creating an emerald."""
        emerald_data = EmeraldLotCreate(
            lot_code="EM001",
            carat=2.5,
            shape="Round",
            color_grade="G",
            clarity="VS1",
            treatment="None",
            origin="Colombia",
            certificate_id="GIA123456",
            status=LotStatus.IN_STOCK
        )
        
        emerald = create_emerald(db_session, emerald_data)
        
        assert emerald.id is not None
        assert emerald.lot_code == "EM001"
        assert emerald.carat == 2.5
        assert emerald.status == LotStatus.IN_STOCK
    
    def test_get_emeralds(self, db_session, sample_emerald):
        """Test getting all emeralds."""
        emeralds = get_emeralds(db_session)
        
        assert len(emeralds) == 1
        assert emeralds[0].id == sample_emerald.id
        assert emeralds[0].lot_code == sample_emerald.lot_code
    
    def test_get_emeralds_with_pagination(self, db_session):
        """Test getting emeralds with pagination."""
        # Create multiple emeralds
        for i in range(5):
            emerald_data = EmeraldLotCreate(
                lot_code=f"EM{i:03d}",
                carat=2.0 + i * 0.5
            )
            create_emerald(db_session, emerald_data)
        
        # Test pagination
        emeralds = get_emeralds(db_session, skip=2, limit=2)
        assert len(emeralds) == 2
    
    def test_get_emerald_by_id(self, db_session, sample_emerald):
        """Test getting emerald by ID."""
        emerald = get_emerald(db_session, sample_emerald.id)
        
        assert emerald is not None
        assert emerald.id == sample_emerald.id
        assert emerald.lot_code == sample_emerald.lot_code
    
    def test_get_emerald_not_found(self, db_session):
        """Test getting non-existent emerald."""
        emerald = get_emerald(db_session, 999)
        assert emerald is None
    
    def test_update_emerald(self, db_session, sample_emerald):
        """Test updating an emerald."""
        update_data = EmeraldLotCreate(
            lot_code="EM001_UPDATED",
            carat=3.0,
            shape="Oval"
        )
        
        updated_emerald = update_emerald(db_session, sample_emerald.id, update_data)
        
        assert updated_emerald.lot_code == "EM001_UPDATED"
        assert updated_emerald.carat == 3.0
        assert updated_emerald.shape == "Oval"
    
    def test_update_emerald_not_found(self, db_session):
        """Test updating non-existent emerald."""
        update_data = EmeraldLotCreate(lot_code="EM001", carat=2.5)
        result = update_emerald(db_session, 999, update_data)
        assert result is None
    
    def test_delete_emerald(self, db_session, sample_emerald):
        """Test deleting an emerald."""
        result = delete_emerald(db_session, sample_emerald.id)
        
        assert result is not None
        assert result.id == sample_emerald.id
        
        # Verify it's deleted
        emerald = get_emerald(db_session, sample_emerald.id)
        assert emerald is None
    
    def test_delete_emerald_not_found(self, db_session):
        """Test deleting non-existent emerald."""
        result = delete_emerald(db_session, 999)
        assert result is None


class TestCounterpartyCRUD:
    """Test counterparty CRUD operations."""
    
    def test_create_counterparty(self, db_session):
        """Test creating a counterparty."""
        cp_data = CounterpartyCreate(
            name="Test Supplier",
            type=CounterpartyType.SUPPLIER,
            contact_info="test@example.com",
            country="Colombia"
        )
        
        counterparty = create_counterparty(db_session, cp_data)
        
        assert counterparty.id is not None
        assert counterparty.name == "Test Supplier"
        assert counterparty.type == CounterpartyType.SUPPLIER
    
    def test_get_counterparties(self, db_session, sample_counterparty):
        """Test getting all counterparties."""
        counterparties = get_counterparties(db_session)
        
        assert len(counterparties) == 1
        assert counterparties[0].id == sample_counterparty.id
    
    def test_get_counterparty_by_id(self, db_session, sample_counterparty):
        """Test getting counterparty by ID."""
        counterparty = get_counterparty(db_session, sample_counterparty.id)
        
        assert counterparty is not None
        assert counterparty.id == sample_counterparty.id
    
    def test_update_counterparty(self, db_session, sample_counterparty):
        """Test updating a counterparty."""
        update_data = CounterpartyUpdate(
            name="Updated Supplier",
            country="Brazil"
        )
        
        updated_cp = update_counterparty(db_session, sample_counterparty.id, update_data)
        
        assert updated_cp.name == "Updated Supplier"
        assert updated_cp.country == "Brazil"
        assert updated_cp.type == sample_counterparty.type  # Unchanged
    
    def test_delete_counterparty(self, db_session, sample_counterparty):
        """Test deleting a counterparty."""
        result = delete_counterparty(db_session, sample_counterparty.id)
        
        assert result is not None
        assert result.id == sample_counterparty.id
        
        # Verify it's deleted
        counterparty = get_counterparty(db_session, sample_counterparty.id)
        assert counterparty is None


class TestTradeCRUD:
    """Test trade CRUD operations."""
    
    def test_create_trade(self, db_session, sample_emerald, sample_counterparty):
        """Test creating a trade."""
        trade_data = TradeCreate(
            type=TradeType.PURCHASE,
            date=date(2024, 1, 15),
            currency="USD",
            unit_price=1000.0,
            total_price=2500.0,
            location="New York",
            emerald_lot_id=sample_emerald.id,
            counterparty_id=sample_counterparty.id
        )
        
        trade = create_trade(db_session, trade_data)
        
        assert trade.id is not None
        assert trade.type == TradeType.PURCHASE
        assert trade.total_price == 2500.0
        assert trade.emerald_lot_id == sample_emerald.id
        assert trade.counterparty_id == sample_counterparty.id
    
    def test_get_trades(self, db_session, sample_trade):
        """Test getting all trades."""
        trades = get_trades(db_session)
        
        assert len(trades) == 1
        assert trades[0].id == sample_trade.id
    
    def test_get_trade_by_id(self, db_session, sample_trade):
        """Test getting trade by ID."""
        trade = get_trade(db_session, sample_trade.id)
        
        assert trade is not None
        assert trade.id == sample_trade.id
    
    def test_update_trade(self, db_session, sample_trade):
        """Test updating a trade."""
        update_data = TradeUpdate(
            total_price=3000.0,
            location="Los Angeles"
        )
        
        updated_trade = update_trade(db_session, sample_trade.id, update_data)
        
        assert updated_trade.total_price == 3000.0
        assert updated_trade.location == "Los Angeles"
        assert updated_trade.type == sample_trade.type  # Unchanged
    
    def test_delete_trade(self, db_session, sample_trade):
        """Test deleting a trade."""
        result = delete_trade(db_session, sample_trade.id)
        
        assert result is not None
        assert result.id == sample_trade.id
        
        # Verify it's deleted
        trade = get_trade(db_session, sample_trade.id)
        assert trade is None


class TestReports:
    """Test reporting functions."""
    
    def test_get_inventory(self, db_session, sample_emerald):
        """Test getting inventory report."""
        inventory = get_inventory(db_session)
        
        assert len(inventory) == 1
        assert inventory[0].id == sample_emerald.id
        assert inventory[0].status == LotStatus.IN_STOCK
    
    def test_get_pnl(self, db_session, sample_emerald, sample_counterparty):
        """Test getting P&L report."""
        # Create purchase trade
        purchase_data = TradeCreate(
            type=TradeType.PURCHASE,
            date=date(2024, 1, 15),
            currency="USD",
            unit_price=1000.0,
            total_price=2500.0,
            emerald_lot_id=sample_emerald.id,
            counterparty_id=sample_counterparty.id
        )
        create_trade(db_session, purchase_data)
        
        # Create sale trade
        sale_data = TradeCreate(
            type=TradeType.SALE,
            date=date(2024, 2, 15),
            currency="USD",
            unit_price=1200.0,
            total_price=3000.0,
            emerald_lot_id=sample_emerald.id,
            counterparty_id=sample_counterparty.id
        )
        create_trade(db_session, sale_data)
        
        pnl = get_pnl(db_session)
        
        assert pnl["total_cost"] == 2500.0
        assert pnl["total_revenue"] == 3000.0
        assert pnl["profit"] == 500.0
    
    def test_get_pnl_no_trades(self, db_session):
        """Test P&L report with no trades."""
        pnl = get_pnl(db_session)
        
        assert pnl["total_cost"] == 0.0
        assert pnl["total_revenue"] == 0.0
        assert pnl["profit"] == 0.0
