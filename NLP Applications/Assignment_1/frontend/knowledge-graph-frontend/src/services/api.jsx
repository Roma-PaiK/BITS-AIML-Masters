// ================================
// src/services/api.js
// Centralized backend API handler
// ================================

import axios from "axios";

// 🔑 Centralized URL
const API_BASE_URL = "http://localhost:5000";

/**
 * Uploads a CSV file to update the graph.
 * Uses axios for consistency and incorporates API_BASE_URL.
 */
export const uploadCSVFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post(`${API_BASE_URL}/upload_csv`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};



export const clearGraph = () => axios.delete(`${API_BASE_URL}/clear_graph`);
export const deleteNode = (id) => axios.delete(`${API_BASE_URL}/delete_node/${id}`);
export const searchNodesLike = (text) => axios.get(`${API_BASE_URL}/query/neighbors/${text}`);
/**
 * Fetches the complete graph data (nodes and edges).
 */
export const getGraphData = async () => {
  return axios.get(`${API_BASE_URL}/api/graph_data`);
};

/**
 * Adds a manual relationship between two nodes.
 */
export const addRelationship = async (u, v) => {
  return axios.post(`${API_BASE_URL}/add_relationship`, { u, v });
};

/**
 * Fetches the immediate connections for a specific node.
 */
export const getNeighbors = async (nodeId) => {
  return axios.get(`${API_BASE_URL}/query/neighbors/${nodeId}`);
};