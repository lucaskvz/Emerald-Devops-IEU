import React, { useEffect, useRef, useState } from "react";
import "./ModalForm.css";

const initialForm = {
  id: null,
  name: "",
  type: "SUPPLIER",
  contact_info: "",
  country: "",
};

export default function CounterpartyFormModal({
  isOpen,
  onClose = () => {},
  onSave,
  initialData,
}) {
  const overlayRef = useRef(null);

  const [form, setForm] = useState(initialForm);

  useEffect(() => {
    if (isOpen) {
      setForm(initialData ? { ...initialForm, ...initialData } : initialForm);
    }
  }, [isOpen, initialData]);

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
    if (typeof onSave === "function") onSave(form);
    doClose();
  };

  const clickOverlay = (e) => {
    if (e.target === overlayRef.current) doClose();
  };

  return (
    <div className="modal-overlay" ref={overlayRef} onClick={clickOverlay}>
      <div className="modal">
        <div className="modal-header">
          <h2>{initialData ? "Edit Counterparty" : "Add Counterparty"}</h2>
          <button className="close-btn" onClick={doClose}>
            ×
          </button>
        </div>

        {/* Fields */}
        <input
          name="name"
          placeholder="Name"
          value={form.name}
          onChange={handleChange}
        />
        <select name="type" value={form.type} onChange={handleChange}>
          <option value="SUPPLIER">Supplier</option>
          <option value="BUYER">Buyer</option>
          <option value="BOTH">Both</option>
        </select>
        <input
          name="contact_info"
          placeholder="Contact Info"
          value={form.contact_info}
          onChange={handleChange}
        />
        <input
          name="country"
          placeholder="Country"
          value={form.country}
          onChange={handleChange}
        />

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
