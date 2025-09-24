import React, { useEffect, useState } from "react";
import { listEmeralds, listCounterparties, listTrades } from "../api";
import axios from "axios";
import DataTable from "../components/DataTable";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

export default function Dashboard() {
  const [emeralds, setEmeralds] = useState([]);
  const [counterparties, setCounterparties] = useState([]);
  const [pnl, setPnl] = useState({ total_cost: 0, total_revenue: 0, profit: 0 });
  const [recentTrades, setRecentTrades] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Get emeralds
        const { data: emeraldData } = await listEmeralds();
        setEmeralds(emeraldData);

        // Get counterparties
        const { data: cpData } = await listCounterparties();
        setCounterparties(cpData);

        // Get P&L
        const { data: pnlData } = await axios.get(`${API_URL}/reports/pnl`);
        setPnl(pnlData);

        // Get trades (latest 5)
        const { data: tradeData } = await listTrades();
        setRecentTrades(tradeData.slice(-5).reverse()); // last 5, newest first
      } catch (e) {
        console.error("Dashboard fetch failed:", e);
      }
    };

    fetchData();
  }, []);

  const tradeColumns = [
    { key: "date", label: "Date" },
    { key: "type", label: "Type" },
    { key: "currency", label: "Currency" },
    { key: "total_price", label: "Total Price" },
    { key: "emerald_lot_id", label: "Emerald Lot ID" },
    { key: "counterparty_id", label: "Counterparty ID" },
  ];

  return (
    <div className="page-content">
      <h1 className="page-title">📊 Dashboard</h1>

      {/* Summary cards */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
          gap: "1rem",
          marginBottom: "2rem",
        }}
      >
        <div className="card">
          <h3>💎 Emeralds in Stock</h3>
          <p>{emeralds.filter((e) => e.status === "IN_STOCK").length}</p>
        </div>

        <div className="card">
          <h3>👥 Counterparties</h3>
          <p>{counterparties.length}</p>
        </div>

        <div className="card">
          <h3>💰 P&L</h3>
          <p>Revenue: ${pnl.total_revenue}</p>
          <p>Cost: ${pnl.total_cost}</p>
          <p>
            Profit:{" "}
            <span style={{ color: pnl.profit >= 0 ? "green" : "red" }}>
              ${pnl.profit}
            </span>
          </p>
        </div>
      </div>

      {/* Recent trades */}
      <h2>Recent Trades</h2>
      <DataTable columns={tradeColumns} data={recentTrades} pageSize={5} />
    </div>
  );
}
