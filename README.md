# Interactive BFS Algorithm Visualization Tool

This project is an interactive web application that visualizes the Breadth-First Search (BFS) algorithm. BFS is a fundamental graph traversal algorithm used to explore nodes in a graph level by level, starting from a given source node.

## Features

- **Graph Input**: Users can input graphs through:
  - Custom edge lists (e.g., "A B, B C, A D")
  - Predefined graph examples (trees, cycles, complete graphs, etc.)
  
- **Interactive Controls**:
  - Choose starting node
  - Adjust execution speed
  - Step through algorithm execution
  - See the complete execution at once
  
- **Visual Representation**:
  - Graph visualization using pygraphviz
  - Color-coding for current node, visited nodes, and queued nodes
  - Step-by-step visualization of BFS execution
  
- **Status Information**:
  - Current node being processed
  - Queue of nodes waiting to be processed
  - Traversal order of visited nodes
  - Step counter
  
- **Educational Elements**:
  - BFS pseudocode with current step highlighting
  - Visual representation of queue operations

## Technologies Used

- **Backend**:
  - Flask web framework
  - Pygraphviz for graph visualization
  - NetworkX for graph data structures
  - Python for core logic
  
- **Frontend**:
  - HTML/CSS for layout and styling
  - JavaScript/jQuery for interactivity
  - Bootstrap for responsive design

## Installation and Setup

1. **Prerequisites**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3 python3-pip graphviz graphviz-dev pkg-config
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the web application**:
   Open your browser and navigate to `http://localhost:8080`

## Usage Guide

1. **Create a Graph**:
   - Select graph type (custom or predefined)
   - For custom graphs, enter edge list in the format "A B, B C, A D"
   - For predefined graphs, select size
   - Click "Create Graph"

2. **Initialize BFS**:
   - Select starting node from dropdown
   - Adjust execution speed if desired
   - Click "Start BFS"

3. **Run BFS**:
   - Use "Step" button to execute one step at a time
   - Use "Complete" button to run BFS to completion
   - Use "Reset" to restart with a new starting node

4. **Observe Visualization**:
   - Red: Current node being processed
   - Green: Previously visited nodes
   - Blue: Nodes in the queue
   - Black: Unvisited nodes

## Project Structure

```
bfs_visualization/
├── app.py               # Flask application
├── bfs.py               # BFS algorithm implementation
├── graph.py             # Graph representation and visualization
├── requirements.txt     # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css    # Application styling
│   └── js/
│       └── script.js    # Frontend interactivity
└── templates/
    └── index.html       # Main page template
```

## Educational Value

This application helps students and learners understand:

- How BFS traverses a graph level by level
- The role of a queue in BFS
- How BFS discovers and processes nodes
- How a BFS tree is formed during traversal
- The relationship between BFS and shortest paths in unweighted graphs