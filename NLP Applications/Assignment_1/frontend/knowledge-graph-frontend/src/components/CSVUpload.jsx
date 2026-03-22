import React, { useState } from "react";
import { uploadCSVFile } from "../services/api";


// src/components/CSVUpload.jsx
const CSVUpload = ({ onUploadSuccess }) => {
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    setStatus("Uploading...");

    try {
      const response = await uploadCSVFile(file);
      setStatus(`Success: Added ${response.total_edges} total edges.`);

      if (onUploadSuccess) onUploadSuccess();

      setTimeout(() => {
        setStatus("");
      }, 3000);

    } catch (error) {
      console.error(error);
      setStatus("Error uploading CSV. Check console.");

      setTimeout(() => {
        setStatus("");
      }, 5000);
    } finally {
      setLoading(false);
      e.target.value = null;
    }
  };

  return (
    <div style={{ border: "1px solid #ddd", padding: "1rem", borderRadius: "8px" }}>
      <h3>Bulk Upload (CSV)</h3>
      <input type="file" accept=".csv" onChange={handleUpload} disabled={loading} />
      {status && (
        <p style={{ 
          color: status.includes("Error") ? "#d32f2f" : "#2e7d32",
          fontWeight: "bold",
          transition: "opacity 0.5s ease" // Optional: makes it feel smoother
        }}>
          {status}
        </p>
      )}
    </div>
  );
};

export default CSVUpload;
