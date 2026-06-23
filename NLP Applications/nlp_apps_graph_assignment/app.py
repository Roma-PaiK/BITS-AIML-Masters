import pandas as pd
import networkx as nx
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# --- 1. Graph Initialization & Data Loading ---
G = nx.Graph()  # Initialize an undirected graph (Twitch friendships are mutual)

def load_data(limit=5000):
    """
    Loads the Twitch Gamers dataset.
    We limit rows for performance during the demo. 
    Set limit=None to load the full dataset (warning: heavy on memory).
    """
    try:
        print(f"Loading Twitch dataset (limit={limit})...")
        # Assuming the file is named 'large_twitch_edges.csv'
        df = pd.read_csv('large_twitch_edges.csv',  nrows=limit)
        
        # The dataset typically has columns like 'numeric_id_1', 'numeric_id_2'
        # We assume standard CSV structure; adjust column names if necessary.
        edges = list(zip(df.iloc[:, 0], df.iloc[:, 1]))
        
        G.add_edges_from(edges)
        print(f"Graph loaded successfully: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges.")
    except FileNotFoundError:
        print("Error: 'large_twitch_edges.csv' not found. Starting with empty graph.")

# Load data on startup
load_data(limit=1000) 

# --- 2. API Endpoints (Graph Management) ---

@app.route('/')
def home():
    """Simple UI to verify the app is running."""
    stats = {
        "Nodes": G.number_of_nodes(),
        "Edges": G.number_of_edges(),
        "Density": round(nx.density(G), 5)
    }
    return render_template_string("""
    <h1>Twitch Knowledge Graph API</h1>
    <p>Graph Status: <b>Active</b></p>
    <ul>
        <li>Nodes: {{ stats.Nodes }}</li>
        <li>Edges: {{ stats.Edges }}</li>
        <li>Density: {{ stats.Density }}</li>
    </ul>
    <h3>Endpoints:</h3>
    <ul>
        <li>POST /add_relationship (JSON: {"u": 1, "v": 2})</li>
        <li>GET /query/neighbors/&lt;node_id&gt;</li>
        <li>GET /query/shortest_path?source=1&target=50</li>
    </ul>
    """, stats=stats)

@app.route('/add_relationship', methods=['POST'])
def add_relationship():
    """
    Endpoint to add a new relationship (edge) between two entities.
    Expects JSON: { "u": "UserA", "v": "UserB" }
    """
    data = request.json
    u = data.get('u')
    v = data.get('v')
    
    if not u or not v:
        return jsonify({"error": "Missing parameters 'u' or 'v'"}), 400
    
    # Add to NetworkX graph
    G.add_edge(u, v)
    
    return jsonify({
        "message": f"Relationship added between {u} and {v}",
        "total_edges": G.number_of_edges()
    }), 201

@app.route('/query/neighbors/<node_id>', methods=['GET'])
def get_neighbors(node_id):
    """
    Query the graph: Find all connections (neighbors) of a specific user.
    Note: Inputs from URL are strings; dataset IDs might be ints.
    """
    # Try converting to int if dataset uses ints, otherwise keep as string
    try:
        real_id = int(node_id)
    except ValueError:
        real_id = node_id

    if real_id not in G:
        return jsonify({"error": "Node not found"}), 404
    
    neighbors = list(G.neighbors(real_id))
    
    # Format for visualization (Nodes + Links)
    response = {
        "central_node": real_id,
        "degree": len(neighbors),
        "neighbors": neighbors
    }
    return jsonify(response), 200

@app.route('/query/shortest_path', methods=['GET'])
def get_shortest_path():
    """
    Advanced Query: Find shortest path between two users.
    Params: ?source=123&target=456
    """
    source = request.args.get('source')
    target = request.args.get('target')
    
    try:
        s = int(source)
        t = int(target)
        if s not in G or t not in G:
             return jsonify({"error": "One or both nodes not found"}), 404
             
        path = nx.shortest_path(G, source=s, target=t)
        return jsonify({"path": path, "length": len(path)-1})
        
    except nx.NetworkXNoPath:
        return jsonify({"error": "No path exists between these users"}), 404
    except ValueError:
        return jsonify({"error": "Invalid node IDs provided"}), 400
    
    
@app.route('/update_user', methods=['POST'])  # or methods=['PUT']
def update_user_endpoint():
    """
    Endpoint to update user details (attributes).
    Expects JSON: { "id": 123, "name": "NewName" }
    """
    data = request.json
    user_id = data.get('id')
    new_name = data.get('name')
    
    # 1. Validate Input
    if not user_id or not new_name:
        return jsonify({"error": "Missing 'id' or 'name'"}), 400
        
    # 2. Call the Logic (The "Update" part)
    # We must convert user_id to int because the CSV loads IDs as ints (usually)
    try:
        uid = int(user_id)
    except ValueError:
        uid = user_id

    if uid in G:
        # This is where the actual NetworkX update happens
        G.nodes[uid]['name'] = new_name
        return jsonify({
            "message": f"User {uid} updated.",
            "current_data": G.nodes[uid]
        }), 200
    else:
        return jsonify({"error": "User not found"}), 404

# --- 3. Run Server ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)