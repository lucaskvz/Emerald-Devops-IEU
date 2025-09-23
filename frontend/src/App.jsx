import React, { useState } from "react";
import "./App.css";
import Emeralds from "./sections/Emeralds";

export default function App() {
  const [active, setActive] = useState("emeralds");

  const menu = [
    { key: "dashboard", label: "📊 Dashboard" },
    { key: "emeralds", label: "💎 Emerald Lots" },
    { key: "counterparties", label: "👥 Counterparties" },
    { key: "trades", label: "🔁 Trades" },
  ];

  return (
    <div className="layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo">Emerald Ledger</div>
        <nav>
          {menu.map((item) => (
            <button
              key={item.key}
              onClick={() => setActive(item.key)}
              className={`menu-btn ${active === item.key ? "active" : ""}`}
            >
              {item.label}
            </button>
          ))}
        </nav>
      </aside>

      {/* Main Content */}
      <main className="content">
        {active === "dashboard" && (
          <h1 className="page-title">📊 Dashboard (coming soon)</h1>
        )}
        {active === "emeralds" && <Emeralds />}
        {active === "counterparties" && (
          <h1 className="page-title">👥 Counterparties (coming soon)</h1>
        )}
        {active === "trades" && (
          <h1 className="page-title">🔁 Trades (coming soon)</h1>
        )}
      </main>
    </div>
  );
}
