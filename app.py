# app.py
from flask import Flask, render_template, request, jsonify
from graph import Graph
from bfs import BFS
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bfs-visualization-secret-key'

# Global objects
graph = Graph()
bfs_algorithm = BFS(graph)

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/create_graph', methods=['POST'])
def create_graph():
    """Create a graph from input or predefined examples."""
    data = request.json
    graph_type = data.get('graph_type')
    
    if graph_type == 'custom':
        edge_list = data.get('edge_list', '')
        graph.parse_edge_list(edge_list)
    else:
        size = int(data.get('size', 5))
        graph.create_predefined_graph(graph_type, size)
    
    # Reset BFS algorithm with the new graph
    bfs_algorithm.reset()
    
    nodes = graph.get_nodes()
    edges = graph.get_edges()
    
    # Generate graph visualization
    graph_image = graph.visualize()
    
    return jsonify({
        'success': True,
        'nodes': nodes,
        'edges': edges,
        'graph_image': graph_image
    })

@app.route('/initialize_bfs', methods=['POST'])
def initialize_bfs():
    """Initialize the BFS algorithm with a starting node."""
    data = request.json
    start_node = data.get('start_node')
    
    if start_node not in graph.get_nodes():
        return jsonify({'success': False, 'error': 'Invalid start node'})
    
    bfs_algorithm.initialize(start_node)
    
    state = bfs_algorithm.get_state()
    graph_image = graph.visualize(
        highlighted_node=state['current_node'],
        visited_nodes=state['visited'],
        queue=state['queue'],
        levels=state['levels']
    )
    
    return jsonify({
        'success': True,
        'state': state,
        'graph_image': graph_image
    })

@app.route('/step_bfs', methods=['POST'])
def step_bfs():
    """Execute one step of the BFS algorithm."""
    success = bfs_algorithm.step()
    
    state = bfs_algorithm.get_state()
    graph_image = graph.visualize(
        highlighted_node=state['current_node'],
        visited_nodes=state['visited'],
        queue=state['queue'],
        levels=state['levels']
    )
    
    return jsonify({
        'success': success,
        'state': state,
        'graph_image': graph_image
    })

@app.route('/complete_bfs', methods=['POST'])
def complete_bfs():
    """Run BFS to completion from the current state."""
    bfs_algorithm.run_to_completion()
    
    state = bfs_algorithm.get_state()
    graph_image = graph.visualize(
        highlighted_node=state['current_node'],
        visited_nodes=state['visited'],
        queue=state['queue'],
        levels=state['levels']
    )
    
    return jsonify({
        'success': True,
        'state': state,
        'graph_image': graph_image
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)