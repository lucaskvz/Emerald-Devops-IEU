import React, { useState } from "react";
import "./DataTable.css";

export default function DataTable({ columns, data = [], pageSize = 10 }) {
  const [page, setPage] = useState(0);

  const start = page * pageSize;
  const end = start + pageSize;
  const pageData = data.slice(start, end);
  const totalPages = Math.max(1, Math.ceil(data.length / pageSize));

  return (
    <div className="datatable">
      <div className="datatable-container">
        <table>
          <thead>
            <tr>
              {columns.map((col) => (
                <th key={col.key}>{col.label}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {pageData.length > 0 ? (
              pageData.map((row, idx) => (
                <tr key={row.id || idx}>
                  {columns.map((col) => (
                    <td key={col.key}>
                      {col.render ? col.render(row) : row[col.key] || ""}
                    </td>
                  ))}
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={columns.length} className="no-records">
                  No records found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="datatable-footer">
        <button
          disabled={page === 0}
          onClick={() => setPage((p) => Math.max(0, p - 1))}
        >
          ◀ Prev
        </button>
        <span>
          Page {page + 1} of {totalPages}
        </span>
        <button
          disabled={page >= totalPages - 1}
          onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
        >
          Next ▶
        </button>
      </div>
    </div>
  );
}
