import React, { useEffect, useState } from "react";
import {
  listTrades,
  createTrade,
  updateTrade,
  deleteTrade,
} from "../api";
import DataTable from "../components/DataTable";
import TradeFormModal from "../components/TradeFormModal";
import ConfirmModal from "../components/ConfirmModal";

export default function Trades() {
  const [trades, setTrades] = useState([]);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isConfirmOpen, setIsConfirmOpen] = useState(false);
  const [selectedTrade, setSelectedTrade] = useState(null);

  // --- Fetch data from backend
  const fetchTrades = async () => {
    try {
      const { data } = await listTrades();
      setTrades(data);
    } catch (e) {
      console.error("Fetch failed:", e);
    }
  };

  useEffect(() => {
    fetchTrades();
  }, []);

  // --- Create + Update
  const handleSave = async (payload) => {
    try {
      if (payload.id) {
        await updateTrade(payload.id, payload); // update
      } else {
        await createTrade(payload); // create
      }
      await fetchTrades();
    } catch (e) {
      console.error("Save failed:", e);
    }
  };

  // --- Delete
  const handleDelete = async () => {
    try {
      if (selectedTrade) {
        await deleteTrade(selectedTrade.id);
        await fetchTrades();
      }
    } catch (e) {
      console.error("Delete failed:", e);
    } finally {
      setIsConfirmOpen(false);
    }
  };

  // --- Table columns
  const columns = [
    { key: "type", label: "Type" },
    { key: "date", label: "Date" },
    { key: "currency", label: "Currency" },
    { key: "unit_price", label: "Unit Price" },
    { key: "total_price", label: "Total Price" },
    { key: "location", label: "Location" },
    { key: "emerald_lot_id", label: "Emerald Lot ID" },
    { key: "counterparty_id", label: "Counterparty ID" },
    {
      key: "actions",
      label: "Actions",
      render: (row) => (
        <div style={{ display: "flex", gap: "0.5rem" }}>
          <button
            className="btn-primary"
            onClick={() => {
              setSelectedTrade(row);
              setIsFormOpen(true);
            }}
          >
            ✏️ Edit
          </button>
          <button
            className="btn-danger"
            onClick={() => {
              setSelectedTrade(row);
              setIsConfirmOpen(true);
            }}
          >
            🗑 Delete
          </button>
        </div>
      ),
    },
  ];

  return (
    <div className="page-content">
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: "1rem",
        }}
      >
        <h1 className="page-title">🔁 Trades</h1>
        <button
          className="btn-primary"
          onClick={() => {
            setSelectedTrade(null);
            setIsFormOpen(true);
          }}
        >
          + Add Trade
        </button>
      </div>

      <DataTable columns={columns} data={trades} pageSize={5} />

      {/* Form modal for create + edit */}
      <TradeFormModal
        isOpen={isFormOpen}
        onClose={() => setIsFormOpen(false)}
        onSave={handleSave}
        initialData={selectedTrade}
      />

      {/* Confirm delete modal */}
      <ConfirmModal
        isOpen={isConfirmOpen}
        onClose={() => setIsConfirmOpen(false)}
        onConfirm={handleDelete}
        message={`Delete trade #${selectedTrade?.id}?`}
      />
    </div>
  );
}
