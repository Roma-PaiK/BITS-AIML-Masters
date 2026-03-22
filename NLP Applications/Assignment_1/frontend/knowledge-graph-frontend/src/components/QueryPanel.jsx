import React, { useState } from "react";
import { searchNodesLike } from "../services/api";

const QueryPanel = ({ onQueryResults }) => {
    const [searchId, setSearchId] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSearch = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const response = await searchNodesLike(searchId);
            onQueryResults(response.data);
        } catch (error) {
            console.error(error);
            alert("Search failed or no matches found.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={panelStyle}>
            <h3>Query Graph</h3>
            <form onSubmit={handleSearch}>
                <input
                    type="text"
                    placeholder="Enter Entity ID (e.g. 123)"
                    value={searchId}
                    onChange={(e) => setSearchId(e.target.value)}
                    style={inputStyle}
                />
                <button type="submit" disabled={loading} style={buttonStyle}>
                    {loading ? "Searching..." : "🔍 Search Connections"}
                </button>
            </form>
        </div>
    );
};

const panelStyle = {
    border: "1px solid #ddd",
    padding: "1rem",
    borderRadius: "8px",
    backgroundColor: "#fefefe",
    marginBottom: "10px"
};

const inputStyle = {
    padding: "8px",
    width: "70%",
    marginRight: "5px",
    borderRadius: "4px",
    border: "1px solid #ccc"
};

const buttonStyle = {
    padding: "8px 12px",
    cursor: "pointer",
    backgroundColor: "#673ab7",
    color: "white",
    border: "none",
    borderRadius: "4px"
};

export default QueryPanel;