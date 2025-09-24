import React, { useEffect, useState } from "react";
import {
  listCounterparties,
  createCounterparty,
  updateCounterparty,
  deleteCounterparty,
} from "../api";
import DataTable from "../components/DataTable";
import CounterpartyFormModal from "../components/CounterpartyFormModal";
import ConfirmModal from "../components/ConfirmModal";

export default function Counterparties() {
  const [counterparties, setCounterparties] = useState([]);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isConfirmOpen, setIsConfirmOpen] = useState(false);
  const [selectedCounterparty, setSelectedCounterparty] = useState(null);

  // --- Fetch data from backend
  const fetchCounterparties = async () => {
    try {
      const { data } = await listCounterparties();
      setCounterparties(data);
    } catch (e) {
      console.error("Fetch failed:", e);
    }
  };

  useEffect(() => {
    fetchCounterparties();
  }, []);

  // --- Create + Update
  const handleSave = async (payload) => {
    try {
      if (payload.id) {
        await updateCounterparty(payload.id, payload); // update
      } else {
        await createCounterparty(payload); // create
      }
      await fetchCounterparties();
    } catch (e) {
      console.error("Save failed:", e);
    }
  };

  // --- Delete
  const handleDelete = async () => {
    try {
      if (selectedCounterparty) {
        await deleteCounterparty(selectedCounterparty.id);
        await fetchCounterparties();
      }
    } catch (e) {
      console.error("Delete failed:", e);
    } finally {
      setIsConfirmOpen(false);
    }
  };

  // --- Table columns
  const columns = [
    { key: "name", label: "Name" },
    { key: "type", label: "Type" },
    { key: "contact_info", label: "Contact Info" },
    { key: "country", label: "Country" },
    {
      key: "actions",
      label: "Actions",
      render: (row) => (
        <div style={{ display: "flex", gap: "0.5rem" }}>
          <button
            className="btn-primary"
            onClick={() => {
              setSelectedCounterparty(row);
              setIsFormOpen(true);
            }}
          >
            ✏️ Edit
          </button>
          <button
            className="btn-danger"
            onClick={() => {
              setSelectedCounterparty(row);
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
        <h1 className="page-title">👥 Counterparties</h1>
        <button
          className="btn-primary"
          onClick={() => {
            setSelectedCounterparty(null);
            setIsFormOpen(true);
          }}
        >
          + Add Counterparty
        </button>
      </div>

      <DataTable columns={columns} data={counterparties} pageSize={5} />

      {/* Form modal */}
      <CounterpartyFormModal
        isOpen={isFormOpen}
        onClose={() => setIsFormOpen(false)}
        onSave={handleSave}
        initialData={selectedCounterparty}
      />

      {/* Confirm delete modal */}
      <ConfirmModal
        isOpen={isConfirmOpen}
        onClose={() => setIsConfirmOpen(false)}
        onConfirm={handleDelete}
        message={`Delete counterparty "${selectedCounterparty?.name}"?`}
      />
    </div>
  );
}
