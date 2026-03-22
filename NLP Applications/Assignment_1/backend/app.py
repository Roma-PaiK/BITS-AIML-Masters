import pandas as pd
import networkx as nx
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# --- Task 5: Setup for single-server production ---
# React build folder is assumed to be in the 'frontend/build' directory
app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
CORS(app)

G = nx.Graph() 

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/query/search/<query_text>', methods=['GET'])
def search_nodes(query_text):
    """
    Finds all nodes that contain the query_text in their ID or Name.
    Returns the nodes and their immediate connections.
    """
    query_text = str(query_text).lower()
    matches = []

    # Find nodes that match the "LIKE" criteria
    for node_id, node_data in G.nodes(data=True):
        name = str(node_data.get('name', '')).lower()
        id_str = str(node_id).lower()
        
        if query_text in name or query_text in id_str:
            matches.append(node_id)

    if not matches:
        return jsonify({"error": "No matches found"}), 404

    # To keep the result clean, let's return the matching nodes 
    # and the edges between them
    subgraph = G.neighbors(matches).copy()
    
    nodes = []
    for n in subgraph.nodes():
        nodes.append({"id": n, "name": G.nodes[n].get('name', str(n))})
        
    links = []
    for u, v, data in subgraph.edges(data=True):
        links.append({"source": u, "target": v, **data})

    return jsonify({
        "nodes": nodes,
        "links": links,
        "match_count": len(matches)
    }), 200

@app.route('/query/neighbors/<node_id>', methods=['GET'])
def get_neighbors(node_id):
    """
    Finds a node and its immediate neighbors, returning them in a 
    format compatible with react-force-graph.
    """
    # 1. Handle ID types (int vs string)
    search_id = int(node_id) if node_id.isdigit() else node_id

    if search_id not in G:
        return jsonify({"error": f"Node {node_id} not found"}), 404
    
    # 2. Identify the nodes to include (the node itself + its neighbors)
    # Using G.neighbors() for your undirected nx.Graph()
    nodes_to_include = {search_id}
    nodes_to_include.update(G.neighbors(search_id))
    
    # 3. Create a Subgraph to get the nodes AND the links between them
    sub = G.subgraph(nodes_to_include)
    
    # 4. Format for Visualization
    nodes_result = []
    for n in sub.nodes():
        node_data = G.nodes[n]
        nodes_result.append({
            "id": n,
            "name": node_data.get('name', str(n)),
            "is_central": n == search_id # For UI highlighting
        })
        
    links_result = []
    for u, v, data in sub.edges(data=True):
        links_result.append({
            "source": u,
            "target": v,
            "relationship": data.get('relationship', 'ROUTE'),
            **data
        })

    return jsonify({
        "nodes": nodes_result,
        "links": links_result,
        "metadata": {
            "central_node": search_id,
            "neighbor_count": len(list(G.neighbors(search_id)))
        }
    }), 200

    
@app.route('/api/graph_data', methods=['GET'])
def get_graph_data_for_visualization():
    """
    Returns generic graph state. 
    Limit prevents UI clutter while the full graph exists in memory for queries.
    """
    limit = request.args.get('limit', default=500, type=int) 

    nodes = []
    links = []
    existing_nodes = set() 
    
    # Process edges with limit for visualization stability
    for i, (u, v, data) in enumerate(G.edges(data=True)):
        if i >= limit:
            break

        links.append({
            "source": u,
            "target": v,
            "relationship": data.get('relationship', 'RELATED_TO'), 
            **data
        })
        
        for node_id in [u, v]:
            if node_id not in existing_nodes:
                node_data = G.nodes.get(node_id, {})
                nodes.append({
                    "id": node_id,
                    "label": "Entity", # Generic label
                    "name": node_data.get('name', str(node_id)), 
                    **node_data
                })
                existing_nodes.add(node_id)
        
    return jsonify({
        "nodes": nodes,
        "links": links,
        "total_graph_edges": G.number_of_edges(),
        "displayed_edges": len(links)
    })

@app.route('/add_relationship', methods=['POST'])
def add_relationship():
    data = request.json
    u, v = data.get('u'), data.get('v')
    rel = data.get('relationship', 'RELATED_TO')
    
    if not u or not v:
        return jsonify({"error": "Missing parameters"}), 400
    
    G.add_edge(u, v, relationship=rel)
    return jsonify({"message": "Relationship added", "total_edges": G.number_of_edges()}), 201

@app.route('/query/search/<query_text>', methods=['GET'])
def search_nodes_fuzzy(query_text):
    query_text = str(query_text).lower()
    
    seed_nodes = []
    for node_id, node_data in G.nodes(data=True):
        name = str(node_data.get('name', '')).lower()
        if query_text in name or query_text in str(node_id).lower():
            seed_nodes.append(node_id)

    print(f"Seeds found: {seed_nodes}", flush=True)

    if not seed_nodes:
        return jsonify({"error": "No matches found"}), 404

    nodes_to_include = set(seed_nodes)
    for n in seed_nodes:
        try:
            if G.is_directed():
                nodes_to_include.update(G.successors(n))
                nodes_to_include.update(G.predecessors(n))
            else:
                nodes_to_include.update(G.neighbors(n))
        except Exception as e:
            print(f"Error finding neighbors for {n}: {e}", flush=True)

    subgraph = G.subgraph(nodes_to_include)
    
    nodes_result = []
    for n in subgraph.nodes():
        node_data = G.nodes[n]
        nodes_result.append({
            "id": n,
            "name": node_data.get('name', str(n)),
            "is_match": n in seed_nodes 
        })
        
    links_result = []
    for u, v, data in subgraph.edges(data=True):
        links_result.append({
            "source": u,
            "target": v,
            "relationship": data.get('relationship', 'CONNECTED_TO')
        })

    print(f"Final Count - Nodes: {len(nodes_result)}, Links: {len(links_result)}", flush=True)

    return jsonify({
        "nodes": nodes_result,
        "links": links_result,
        "match_count": len(seed_nodes)
    }), 200


@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    try:
        df = pd.read_csv(file, encoding='latin1')
        
        for _, row in df.iterrows():
            u, v = row.iloc[0], row.iloc[1]
            attrs = row.iloc[2:].to_dict()
            clean_attrs = {k: v for k, v in attrs.items() if pd.notna(v)}
            G.add_edge(u, v, **clean_attrs)
            
        return jsonify({
            "message": "CSV uploaded and graph updated", 
            "total_edges": G.number_of_edges(),
            "total_nodes": G.number_of_nodes()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/clear_graph', methods=['DELETE'])
def clear_graph():
    """Wipes the entire graph from memory."""
    G.clear()
    return jsonify({
        "message": "Graph cleared successfully",
        "total_nodes": 0,
        "total_edges": 0
    }), 200

@app.route('/delete_node/<node_id>', methods=['DELETE'])
def delete_node(node_id):
    """Deletes a specific node and its associated edges."""
    try:
        # Match the ID type (int if numeric, else string)
        search_id = int(node_id) if node_id.isdigit() else node_id
        
        if G.has_node(search_id):
            G.remove_node(search_id)
            return jsonify({"message": f"Node {node_id} deleted"}), 200
        else:
            return jsonify({"error": "Node not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)