# Distance Vector Routing Simulator

## Introduction

The **Distance Vector Routing Simulator** is an educational project developed in Python using the **Tkinter** library to provide an interactive graphical interface. The main goal is to help users understand the distance vector routing algorithm, a fundamental method for determining optimal paths between nodes in a network.

With this simulator, users can:
- Create a network by adding nodes and links.
- Assign costs to links.
- Observe how nodes dynamically update their routing tables.

## Project Architecture

The project is structured into four main modules for modularity and maintainability:

1. **node.py**: Defines the `Node` class, representing a network node. Each node maintains a list of neighbors and a routing table.
2. **routing_table.py**: Manages routing table updates using the distance vector algorithm.
3. **gui.py**: Implements the graphical interface using Tkinter, allowing users to interact with the network.
4. **main.py**: The application's entry point, launching the main window and connecting components.

## GUI Features

- **Add Nodes and Links**: Use buttons at the bottom to add nodes and links.
- **Validation Checks**: Prevents duplicate links or negative weights.
- **View Routing Tables**: Right-click a node to view its routing table.
- **Modify Links**: Remove a link by selecting it and left-clicking.
- **Rename Nodes**: Double-click a node to rename it.
- **Drag Nodes**: Move nodes by dragging them with the mouse.
- **Zoom**: Supports zoom for better network visualization.

## Usage Examples

1. **Add a Node**:
   - Click "Add Node" and select a position in the window.

2. **Add a Link**:
   - Click "Add Link", select two nodes, and enter the link cost.

3. **View Routing Table**:
   - Right-click a node to view its routing table.

4. **Remove a Link**:
   - Select a link and left-click to remove it.

## Solved Issues

During development, several issues were addressed:
- **Routing Table Updates**: Tables didn't update correctly when link costs changed. An explicit check was added to force updates.
- **Duplicate Links**: Prevents creating multiple links between the same nodes.

## Installation and Execution

1. **Requirements**:
   - Python 3.x
   - Tkinter library (usually included with Python)

2. **Execution**:
   - Clone the repository:
     ```bash
     git clone https://github.com/your-repository/distance-vector-simulator.git
     ```
   - Navigate to the project folder:
     ```bash
     cd distance-vector-simulator
     ```
   - Run `main.py`:
     ```bash
     python main.py
     ```

## Conclusion

The **Distance Vector Routing Simulator** is a powerful educational tool for understanding network routing principles. Its intuitive interface and dynamic routing table updates provide an engaging learning experience. Future enhancements could include saving network topologies or implementing additional routing algorithms.
