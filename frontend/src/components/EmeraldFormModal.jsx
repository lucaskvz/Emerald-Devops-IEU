import React, { useEffect, useRef, useState } from "react";
import "./ModalForm.css";

// Constants
const VALID_STATUSES = ["IN_STOCK", "SOLD"];

const initialForm = {
  lot_code: "",
  carat: "",
  shape: "",
  color_grade: "",
  clarity: "",
  treatment: "",
  origin: "",
  certificate_id: "",
  status: "IN_STOCK",
};

// Data transformation utility (Single Responsibility Principle)
const transformFormDataToPayload = (formData) => {
  const payload = { ...formData };
  
  // Convert carat from string to float (required field)
  if (payload.carat === "" || payload.carat === null || payload.carat === undefined) {
    throw new Error("Carat is required and must be a number");
  }
  payload.carat = parseFloat(payload.carat);
  if (isNaN(payload.carat)) {
    throw new Error("Carat must be a valid number");
  }
  
  // Validate lot_code (required field)
  if (!payload.lot_code || payload.lot_code.trim() === "") {
    throw new Error("Lot code is required");
  }
  payload.lot_code = payload.lot_code.trim();
  
  // Convert empty strings to null for optional fields
  const optionalStringFields = ["shape", "color_grade", "clarity", "treatment", "origin", "certificate_id"];
  optionalStringFields.forEach(field => {
    if (payload[field] === "") {
      payload[field] = null;
    }
  });
  
  // Validate and normalize status
  if (!VALID_STATUSES.includes(payload.status)) {
    payload.status = "IN_STOCK"; // Default to valid status
  }
  
  return payload;
};

export default function EmeraldFormModal({
  isOpen,
  onClose = () => {},
  onSave,
  onSubmit, // backward compat
  initialData, // 👈 allows editing
}) {
  const overlayRef = useRef(null);

  const [step, setStep] = useState(0);
  const [form, setForm] = useState(initialForm);

  // --- Load data into form when modal opens ---
  useEffect(() => {
    if (isOpen) {
      if (initialData) {
        // Convert API response data to form format (handle type conversions)
        const formData = {
          ...initialForm,
          ...initialData,
          // Ensure carat is a string for the input field
          carat: initialData.carat != null ? String(initialData.carat) : "",
          // Ensure optional fields are strings or empty
          shape: initialData.shape || "",
          color_grade: initialData.color_grade || "",
          clarity: initialData.clarity || "",
          treatment: initialData.treatment || "",
          origin: initialData.origin || "",
          certificate_id: initialData.certificate_id || "",
        };
        setForm(formData);
      } else {
        setForm(initialForm);
      }
      setStep(0);
    }
  }, [isOpen, initialData]);

  const doClose = () => {
    setForm(initialForm);
    setStep(0);
    onClose();
  };

  // ✅ Close on ESC (no eslint warning anymore)
  useEffect(() => {
    if (!isOpen) return;
    const handler = (e) => {
      if (e.key === "Escape") {
        setForm(initialForm);
        setStep(0);
        onClose();
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const next = () => setStep((s) => Math.min(s + 1, 2));
  const prev = () => setStep((s) => Math.max(s - 1, 0));

  const doSave = () => {
    try {
      // Transform and validate form data
      const payload = transformFormDataToPayload(form);
      
      const handler = typeof onSave === "function" ? onSave : onSubmit;
      if (typeof handler === "function") handler(payload);
      doClose();
    } catch (error) {
      // Show validation error to user
      alert(error.message || "Please fill in all required fields");
    }
  };

  const clickOverlay = (e) => {
    if (e.target === overlayRef.current) doClose();
  };

  return (
    <div className="modal-overlay" ref={overlayRef} onClick={clickOverlay}>
      <div className="modal">
        {/* Header with close button */}
        <div className="modal-header">
          <h2>{initialData ? "Edit Emerald" : "Add New Emerald"}</h2>
          <button className="close-btn" onClick={doClose}>
            ×
          </button>
        </div>

        {/* STEP 0 */}
        {step === 0 && (
          <>
            <input
              name="lot_code"
              required
              placeholder="Lot Code"
              value={form.lot_code}
              onChange={handleChange}
              disabled={!!initialData} // 👈 prevent editing lot_code when editing
            />
            <input
              name="carat"
              type="number"
              step="0.01"
              min="0"
              required
              placeholder="Carat"
              value={form.carat}
              onChange={handleChange}
            />
            <select name="shape" value={form.shape} onChange={handleChange}>
              <option value="">-- Select Shape --</option>
              <option value="Round">Round</option>
              <option value="Oval">Oval</option>
              <option value="Emerald Cut">Emerald Cut</option>
              <option value="Princess">Princess</option>
              <option value="Cushion">Cushion</option>
              <option value="Pear">Pear</option>
              <option value="Marquise">Marquise</option>
              <option value="Radiant">Radiant</option>
              <option value="Asscher">Asscher</option>
              <option value="Heart">Heart</option>
              <option value="Uncut">Uncut / Rough</option>
            </select>
          </>
        )}

        {/* STEP 1 */}
        {step === 1 && (
          <>
            <select
              name="color_grade"
              value={form.color_grade}
              onChange={handleChange}
            >
              <option value="">-- Select Color Grade --</option>
              <option value="AAA">AAA (Top)</option>
              <option value="AA">AA (Fine)</option>
              <option value="A">A (Good)</option>
              <option value="B">B (Commercial)</option>
            </select>

            <select
              name="clarity"
              value={form.clarity}
              onChange={handleChange}
            >
              <option value="">-- Select Clarity --</option>
              <option value="IF">IF (Internally Flawless)</option>
              <option value="VVS">VVS</option>
              <option value="VS">VS</option>
              <option value="SI">SI</option>
              <option value="I">I (Included)</option>
            </select>

            <input
              name="treatment"
              placeholder="Treatment (e.g. Oil, Resin, None)"
              value={form.treatment}
              onChange={handleChange}
            />
          </>
        )}

        {/* STEP 2 */}
        {step === 2 && (
          <>
            <input
              name="origin"
              placeholder="Origin (e.g. Colombia, Zambia, Brazil)"
              value={form.origin}
              onChange={handleChange}
            />
            <input
              name="certificate_id"
              placeholder="Certificate ID"
              value={form.certificate_id}
              onChange={handleChange}
            />
            <select name="status" value={form.status} onChange={handleChange}>
              <option value="IN_STOCK">In Stock</option>
              <option value="SOLD">Sold</option>
            </select>
          </>
        )}

        {/* Actions */}
        <div className="modal-actions">
          {step > 0 && (
            <button type="button" className="secondary" onClick={prev}>
              ⬅ Back
            </button>
          )}
          {step < 2 ? (
            <button type="button" className="primary" onClick={next}>
              Next ➡
            </button>
          ) : (
            <button type="button" className="primary" onClick={doSave}>
              {initialData ? "Update" : "Save"}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
