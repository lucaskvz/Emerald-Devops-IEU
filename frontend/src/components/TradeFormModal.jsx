import React, { useEffect, useRef, useState } from "react";
import "./ModalForm.css";
import { listEmeralds, listCounterparties } from "../api";  // ✅ import API calls

const initialForm = {
  id: null,
  type: "PURCHASE",
  date: "",
  currency: "USD",
  unit_price: "",
  total_price: "",
  location: "",
  emerald_lot_id: "",
  counterparty_id: "",
};

export default function TradeFormModal({
  isOpen,
  onClose = () => {},
  onSave,
  initialData,
}) {
  const overlayRef = useRef(null);
  const [form, setForm] = useState(initialForm);

  const [emeralds, setEmeralds] = useState([]);
  const [counterparties, setCounterparties] = useState([]);

  // Reset form when modal opens
  useEffect(() => {
    if (isOpen) {
      setForm(initialData ? { ...initialForm, ...initialData } : initialForm);

      // ✅ fetch emeralds + counterparties only when modal opens
      fetchEmeralds();
      fetchCounterparties();
    }
  }, [isOpen, initialData]);

  const fetchEmeralds = async () => {
    try {
      const { data } = await listEmeralds();
      setEmeralds(data);
    } catch (e) {
      console.error("Failed to fetch emeralds:", e);
    }
  };

  const fetchCounterparties = async () => {
    try {
      const { data } = await listCounterparties();
      setCounterparties(data);
    } catch (e) {
      console.error("Failed to fetch counterparties:", e);
    }
  };

  const doClose = () => {
    setForm(initialForm);
    onClose();
  };

  // Close on ESC
  useEffect(() => {
    if (!isOpen) return;
    const handler = (e) => e.key === "Escape" && doClose();
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [isOpen]);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSave = () => {
    // ✅ Cast IDs and prices to proper types
    const payload = {
      ...form,
      unit_price: form.unit_price ? parseFloat(form.unit_price) : null,
      total_price: form.total_price ? parseFloat(form.total_price) : null,
      emerald_lot_id: form.emerald_lot_id ? parseInt(form.emerald_lot_id, 10) : null,
      counterparty_id: form.counterparty_id ? parseInt(form.counterparty_id, 10) : null,
    };

    if (typeof onSave === "function") onSave(payload);
    doClose();
  };

  const clickOverlay = (e) => {
    if (e.target === overlayRef.current) doClose();
  };

  return (
    <div className="modal-overlay" ref={overlayRef} onClick={clickOverlay}>
      <div className="modal">
        <div className="modal-header">
          <h2>{initialData ? "Edit Trade" : "Add Trade"}</h2>
          <button className="close-btn" onClick={doClose}>
            ×
          </button>
        </div>

        {/* Fields */}
        <select name="type" value={form.type} onChange={handleChange}>
          <option value="PURCHASE">Purchase</option>
          <option value="SALE">Sale</option>
        </select>

        <input type="date" name="date" value={form.date} onChange={handleChange} />
        <input name="currency" placeholder="Currency" value={form.currency} onChange={handleChange} />
        <input type="number" name="unit_price" placeholder="Unit Price" value={form.unit_price} onChange={handleChange} />
        <input type="number" name="total_price" placeholder="Total Price" value={form.total_price} onChange={handleChange} />
        <input name="location" placeholder="Location" value={form.location} onChange={handleChange} />

        {/* ✅ Dropdown for Emeralds */}
        <select
          name="emerald_lot_id"
          value={form.emerald_lot_id}
          onChange={handleChange}
        >
          <option value="">-- Select Emerald Lot --</option>
          {emeralds.map((e) => (
            <option key={e.id} value={e.id}>
              {e.id} – {e.carat} ct
            </option>
          ))}
        </select>

        {/* ✅ Dropdown for Counterparties */}
        <select
          name="counterparty_id"
          value={form.counterparty_id}
          onChange={handleChange}
        >
          <option value="">-- Select Counterparty --</option>
          {counterparties.map((c) => (
            <option key={c.id} value={c.id}>
              {c.id} – {c.name}
            </option>
          ))}
        </select>

        {/* Actions */}
        <div className="modal-actions">
          <button type="button" className="primary" onClick={handleSave}>
            {initialData ? "Update" : "Save"}
          </button>
        </div>
      </div>
    </div>
  );
}
