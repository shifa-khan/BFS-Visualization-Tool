# bfs.py
from collections import deque

class BFS:
    def __init__(self, graph):
        self.graph = graph
        self.reset()
        
    def reset(self):
        """Reset the BFS state for a new run."""
        self.visited = []          # List of visited nodes in order
        self.queue = deque()       # Current queue
        self.current_node = None   # Current node being processed
        self.levels = {}           # Dictionary mapping nodes to their BFS tree level
        self.parent = {}           # Dictionary mapping nodes to their parent in BFS tree
        self.step_count = 0        # Counter for steps executed
        self.finished = False      # Flag to indicate if BFS is complete
        
    def initialize(self, start_node):
        """Initialize BFS with a starting node."""
        self.reset()
        self.queue.append(start_node)
        self.levels[start_node] = 0
        self.parent[start_node] = None
        
    def step(self):
        """Execute one step of the BFS algorithm."""
        if self.finished or not self.queue:
            self.finished = True
            return False
            
        self.step_count += 1
        
        # Dequeue a vertex from queue
        self.current_node = self.queue.popleft()
        
        # Mark as visited if not already
        if self.current_node not in self.visited:
            self.visited.append(self.current_node)
            
        # Get all adjacent vertices
        for neighbor in self.graph.get_neighbors(self.current_node):
            # If not visited, mark it and enqueue it
            if neighbor not in self.visited and neighbor not in self.queue:
                self.queue.append(neighbor)
                self.levels[neighbor] = self.levels[self.current_node] + 1
                self.parent[neighbor] = self.current_node
                
        return True
        
    def run_to_completion(self):
        """Run BFS to completion from the current state."""
        while not self.finished and self.step():
            pass
        
    def get_state(self):
        """Return the current state of the BFS algorithm."""
        return {
            "visited": self.visited.copy(),
            "queue": list(self.queue),
            "current_node": self.current_node,
            "levels": self.levels.copy(),
            "step_count": self.step_count,
            "finished": self.finished
        }
        
    def get_bfs_tree(self):
        """Get the BFS tree from the parent dictionary."""
        tree_edges = []
        for node, parent in self.parent.items():
            if parent is not None:
                tree_edges.append((parent, node))
        return tree_edges