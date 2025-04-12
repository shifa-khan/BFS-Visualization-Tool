# graph.py
import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz as pgv
import io
import base64
from matplotlib.colors import to_rgba

class Graph:
    def __init__(self):
        self.graph = nx.Graph()
        
    def add_edge(self, u, v):
        self.graph.add_edge(u, v)
        
    def add_node(self, node):
        self.graph.add_node(node)
        
    def parse_edge_list(self, edge_list_str):
        """Parse a string representation of an edge list and build the graph."""
        self.graph.clear()
        edges = edge_list_str.split(',')
        for edge in edges:
            # Strip whitespace and split on space
            nodes = edge.strip().split()
            if len(nodes) == 2:
                u, v = nodes
                self.add_edge(u, v)
            elif len(nodes) == 1 and nodes[0]:  # Add isolated node
                self.add_node(nodes[0])
                
    def get_nodes(self):
        return list(self.graph.nodes())
    
    def get_edges(self):
        return list(self.graph.edges())
    
    def get_neighbors(self, node):
        return list(self.graph.neighbors(node))
    
    def visualize(self, highlighted_node=None, visited_nodes=None, queue=None, levels=None):
        """Generate visualization of the graph with optional highlighting."""
        if visited_nodes is None:
            visited_nodes = []
        if queue is None:
            queue = []
        if levels is None:
            levels = {}
            
        # Create a PyGraphviz graph
        G_viz = pgv.AGraph(strict=False, directed=False)
        
        # Add nodes
        for node in self.graph.nodes():
            if node == highlighted_node:
                G_viz.add_node(node, color="red", style="filled", fillcolor="red", fontcolor="white")
            elif node in queue:
                G_viz.add_node(node, color="blue", style="filled", fillcolor="lightblue")
            elif node in visited_nodes:
                G_viz.add_node(node, color="green", style="filled", fillcolor="lightgreen")
            else:
                G_viz.add_node(node, color="black")
                
        # Add edges
        for u, v in self.graph.edges():
            G_viz.add_edge(u, v)
            
        # Layout using dot
        G_viz.layout(prog='dot')
        
        # Save to a temporary file and read back
        img_data = G_viz.draw(format='png')
        
        # Encode the image to base64 for web display
        encoded = base64.b64encode(img_data).decode('utf-8')
        return encoded
        
    def create_predefined_graph(self, graph_type, size=5):
        """Create a predefined graph based on the type."""
        self.graph.clear()
        
        if graph_type == "tree":
            self.graph = nx.balanced_tree(2, 2)  # Binary tree of depth 2
        elif graph_type == "cycle":
            self.graph = nx.cycle_graph(size)
        elif graph_type == "complete":
            self.graph = nx.complete_graph(size)
        elif graph_type == "path":
            self.graph = nx.path_graph(size)
        elif graph_type == "star":
            self.graph = nx.star_graph(size - 1)
        
        # Relabel nodes to be strings (letters) instead of numbers
        mapping = {i: chr(65 + i) for i in range(min(26, len(self.graph)))}
        self.graph = nx.relabel_nodes(self.graph, mapping)