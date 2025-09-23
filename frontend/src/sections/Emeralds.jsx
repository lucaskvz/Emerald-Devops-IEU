import React, { useEffect, useState } from "react";
import {
  listEmeralds,
  createEmerald,
  updateEmerald,
  deleteEmerald,
} from "../api";
import DataTable from "../components/DataTable";
import EmeraldFormModal from "../components/EmeraldFormModal";
import ConfirmModal from "../components/ConfirmModal";

export default function Emeralds() {
  const [emeralds, setEmeralds] = useState([]);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isConfirmOpen, setIsConfirmOpen] = useState(false);
  const [selectedEmerald, setSelectedEmerald] = useState(null);

  // --- Fetch data from backend
  const fetchEmeralds = async () => {
    try {
      const { data } = await listEmeralds();
      setEmeralds(data);
    } catch (e) {
      console.error("Fetch failed:", e);
    }
  };

  useEffect(() => {
    fetchEmeralds();
  }, []);

  // --- Create + Update
  const handleSave = async (payload) => {
    try {
      if (payload.id) {
        await updateEmerald(payload.id, payload); // update
      } else {
        await createEmerald(payload); // create
      }
      await fetchEmeralds();
    } catch (e) {
      console.error("Save failed:", e);
    }
  };

  // --- Delete
  const handleDelete = async () => {
    try {
      if (selectedEmerald) {
        await deleteEmerald(selectedEmerald.id);
        await fetchEmeralds();
      }
    } catch (e) {
      console.error("Delete failed:", e);
    } finally {
      setIsConfirmOpen(false);
    }
  };

  // --- Table columns (no notes anymore)
  const columns = [
    { key: "lot_code", label: "Lot Code" },
    { key: "carat", label: "Carat" },
    { key: "shape", label: "Shape" },
    { key: "color_grade", label: "Color Grade" },
    { key: "clarity", label: "Clarity" },
    { key: "treatment", label: "Treatment" },
    { key: "origin", label: "Origin" },
    { key: "certificate_id", label: "Certificate ID" },
    { key: "status", label: "Status" },
    {
      key: "actions",
      label: "Actions",
      render: (row) => (
        <div style={{ display: "flex", gap: "0.5rem" }}>
          <button
            className="btn-primary"
            onClick={() => {
              setSelectedEmerald(row);
              setIsFormOpen(true);
            }}
          >
            ✏️ Edit
          </button>
          <button
            className="btn-danger"
            onClick={() => {
              setSelectedEmerald(row);
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
        <h1 className="page-title">💎 Emerald Lots</h1>
        <button
          className="btn-primary"
          onClick={() => {
            setSelectedEmerald(null);
            setIsFormOpen(true);
          }}
        >
          + Add Emerald
        </button>
      </div>

      <DataTable columns={columns} data={emeralds} pageSize={5} />

      {/* Form modal for create + edit */}
      <EmeraldFormModal
        isOpen={isFormOpen}
        onClose={() => setIsFormOpen(false)}
        onSave={handleSave}
        initialData={selectedEmerald}
      />

      {/* Confirm delete modal */}
      <ConfirmModal
        isOpen={isConfirmOpen}
        onClose={() => setIsConfirmOpen(false)}
        onConfirm={handleDelete}
        message={`Delete emerald "${selectedEmerald?.lot_code}"?`}
      />
    </div>
  );
}
