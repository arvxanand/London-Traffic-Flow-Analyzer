# London Traffic Flow Analyzer & Route Planner

A Python project that fetches real-time traffic data from the UK National Highways WebTRIS API and uses it to analyze traffic patterns and plan optimal routes between London Gatwick and London Heathrow airports.

## Features

### Traffic Analysis
- Fetch real sensor data from the WebTRIS API
- Compute average speeds and traffic volumes
- Identify peak traffic hours
- Analyze traffic conditions by hour

### Route Planning
- Models the M25 road network as a weighted graph
- Uses real-time traffic speeds as edge weights (travel time in minutes)
- Compares three possible routes from Gatwick to Heathrow:
  - Route A: Direct M25 (J7 → J12 → J13 → J14 → Heathrow)
  - Route B: M25 to J12, then local roads via Sunbury
  - Route C: M25 to J13, then A30 via Staines
- Implements three pathfinding algorithms from scratch:
  - Breadth-First Search (BFS) — finds the route with the fewest junctions
  - Depth-First Search (DFS) — finds any valid route
  - Dijkstra's Algorithm — finds the fastest route based on real traffic data

## Technologies
- Python
- REST APIs
- Graph data structures
- Pathfinding algorithms
- Object-Oriented Design