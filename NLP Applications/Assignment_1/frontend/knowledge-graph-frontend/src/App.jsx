import React, { useState, useEffect, useCallback } from "react";
import "./App.css";
import CSVUpload from "./components/CSVUpload";
import ManualInput from "./components/ManualInput";
import QueryPanel from "./components/QueryPanel";
import GraphView from "./components/GraphView";
import { getGraphData, clearGraph } from "./services/api";

const App = () => {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [isCollapsed, setIsCollapsed] = useState(false);

  const refreshGraph = useCallback(async () => {
    try {
      const response = await getGraphData();
      setGraphData({ ...response.data });
    } catch (error) {
      console.error("Sync Error:", error);
    }
  }, []);

  useEffect(() => {
    refreshGraph();
  }, [refreshGraph]);

  const handleQueryResult = (data) => {
    console.log("Search Result received:", data);

    if (data.nodes && data.links) {
      setGraphData({
        nodes: [...data.nodes],
        links: [...data.links]
      });

      console.log(`Visualizing ${data.metadata.neighbor_count} connections for ${data.metadata.central_node}`);
    } else {
      console.error("API response missing nodes or links array");
      alert("Error: Received invalid data format from server.");
    }
  };

  return (
    <div className="app-container">
      <aside className={`sidebar ${isCollapsed ? "collapsed" : ""}`}>
        <header>
          <h2 style={{ color: "var(--primary-color)", margin: 0 }}>KnowledgeGraph</h2>
          <p style={{ color: "var(--text-muted)", fontSize: "0.8rem" }}>v1.0 • Live Dashboard</p>
        </header>

        <section className="sidebar-section">
          <h3>Search & Filter</h3>
          <QueryPanel onQueryResults={handleQueryResult} />
          <button
            onClick={refreshGraph}
            style={{ width: '100%', marginTop: '10px', padding: '10px', background: '#fff', border: '1px solid #e2e8f0' }}
          >
            Reset Visualization
          </button>
        </section>

        <section className="sidebar-section">
          <h3>Add Entity</h3>
          <ManualInput onDataAdded={refreshGraph} />
        </section>

        <section className="sidebar-section">
          <h3>Bulk Import</h3>
          <CSVUpload onUploadSuccess={refreshGraph} />
        </section>

        <button className="clear-btn" onClick={async () => {
          if (window.confirm("Delete all graph data?")) {
            await clearGraph();
            refreshGraph();
          }
        }}>
          Clear All Knowledge
        </button>
      </aside>

      <main className="main-content">
        <button
          className="collapse-toggle-btn"
          onClick={() => setIsCollapsed(!isCollapsed)}
        >
          {isCollapsed ? "❯" : "❮"}
        </button>

        <div className="stats-overlay">
          Active Nodes: {graphData.nodes.length} | Edges: {graphData.links.length}
        </div>

        <div className="graph-container">
          <GraphView graphData={graphData} />
        </div>
      </main>
    </div>
  );
};

export default App;