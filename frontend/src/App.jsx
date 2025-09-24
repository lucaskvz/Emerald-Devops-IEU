import React, { useState } from "react";
import "./App.css";

// Import each section (full-page views)
import Dashboard from "./sections/Dashboard";
import Emeralds from "./sections/Emeralds";
import Counterparties from "./sections/Counterparties";
import Trades from "./sections/Trades";

export default function App() {
  // Default to dashboard when app loads
  const [active, setActive] = useState("dashboard");

  // Sidebar menu items
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
        {active === "dashboard" && <Dashboard />}
        {active === "emeralds" && <Emeralds />}
        {active === "counterparties" && <Counterparties />}
        {active === "trades" && <Trades />}
      </main>
    </div>
  );
}
