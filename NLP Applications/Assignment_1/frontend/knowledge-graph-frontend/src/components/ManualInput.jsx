import React, { useState } from "react";
import { addRelationship } from "../services/api";

const ManualInput = ({ onDataAdded }) => {
  const [entity1, setEntity1] = useState("");
  const [entity2, setEntity2] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async () => {
    if (!entity1 || !entity2) {
      setMessage("Both entities are required.");
      setTimeout(() => setMessage(""), 5000);
      return;
    }

    try {
      await addRelationship(entity1, entity2);
      
      // Trigger the graph refresh in App.jsx
      if (onDataAdded) onDataAdded(); 
      
      setMessage("✅ Relationship added successfully!");
      setEntity1("");
      setEntity2("");

      // ⏱️ Clear success message after 5 seconds
      setTimeout(() => {
        setMessage("");
      }, 5000);

    } catch (error) {
      setMessage("❌ Error adding relationship.");
      // ⏱️ Clear error message after 5 seconds
      setTimeout(() => {
        setMessage("");
      }, 5000);
    }
  };

  return (
    <div className="manual-input-container">
      <h3>Manual Relationship Entry</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        <input
          placeholder="Entity 1 ID (e.g., Station A)"
          value={entity1}
          onChange={(e) => setEntity1(e.target.value)}
        />
        <input
          placeholder="Entity 2 ID (e.g., Station B)"
          value={entity2}
          onChange={(e) => setEntity2(e.target.value)}
        />
        <button 
          onClick={handleSubmit}
          style={{ 
            backgroundColor: "var(--primary-color)", 
            color: "white", 
            border: "none",
            padding: "10px",
            marginTop: "5px"
          }}
        >
          Add Connection
        </button>
      </div>
      
      {message && (
        <p style={{ 
          fontSize: "0.85rem", 
          marginTop: "10px", 
          color: message.includes("Error") || message.includes("required") ? "var(--danger-color)" : "#2e7d32",
          fontWeight: "500"
        }}>
          {message}
        </p>
      )}
    </div>
  );
};

export default ManualInput;