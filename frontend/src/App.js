import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [emeralds, setEmeralds] = useState([]);
  const [form, setForm] = useState({ lot_code: "", carat: "" });
  const API_URL = "http://127.0.0.1:8000";

  // Fetch emeralds
  const fetchEmeralds = async () => {
    try {
      const res = await axios.get(`${API_URL}/emeralds/`);
      setEmeralds(res.data);
    } catch (err) {
      console.error("Error fetching:", err);
    }
  };

  useEffect(() => {
    fetchEmeralds();
  }, []);

  // Add emerald
  const addEmerald = async () => {
    if (!form.lot_code || !form.carat) return;
    try {
      await axios.post(`${API_URL}/emeralds/`, form);
      setForm({ lot_code: "", carat: "" });
      fetchEmeralds();
    } catch (err) {
      console.error("Error adding:", err);
    }
  };

  // Delete emerald
  const deleteEmerald = async (id) => {
    try {
      await axios.delete(`${API_URL}/emeralds/${id}`);
      fetchEmeralds();
    } catch (err) {
      console.error("Error deleting:", err);
    }
  };

  return (
    <div className="container">
      <h1>💎 Emerald Ledger</h1>

      {/* Form */}
      <div className="form">
        <input
          placeholder="Lot Code"
          value={form.lot_code}
          onChange={(e) => setForm({ ...form, lot_code: e.target.value })}
        />
        <input
          type="number"
          placeholder="Carat"
          value={form.carat}
          onChange={(e) => setForm({ ...form, carat: e.target.value })}
        />
        <button onClick={addEmerald}>Add Emerald</button>
      </div>

      {/* List */}
      <ul className="list">
        {emeralds.length === 0 ? (
          <li>No emeralds yet.</li>
        ) : (
          emeralds.map((e) => (
            <li key={e.id} className="item">
              <span>
                {e.lot_code} — {e.carat} ct [{e.status}]
              </span>
              <button onClick={() => deleteEmerald(e.id)}>Delete</button>
            </li>
          ))
        )}
      </ul>
    </div>
  );
}

export default App;
