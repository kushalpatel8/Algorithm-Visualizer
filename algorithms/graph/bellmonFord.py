def bellman_ford(graph, start_node=0, end_node=None):
    nodes = list(graph.keys())
    distances = {node: float('inf') for node in nodes}
    distances[start_node] = 0
    visited = {start_node}
    
    yield start_node, visited, distances, None, f"Initialized: start node {start_node} distance = 0"
    
    # Relax edges |V| - 1 times
    for i in range(len(nodes) - 1):
        updated = False
        for u in nodes:
            if distances[u] == float('inf'):
                continue
            for v, weight in graph[u].items():
                visited.add(u)
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    visited.add(v)
                    updated = True
                    yield v, visited, distances, (u, v), f"Pass {i+1}: Relaxed ({u}->{v}, w={weight}), dist[{v}] = {distances[v]}"
                else:
                    yield u, visited, distances, (u, v), f"Pass {i+1}: Evaluated ({u}->{v}, w={weight}), dist[{v}] remains {distances[v]}"
        if not updated:
            break
            
    # Check for negative weight cycles
    for u in nodes:
        if distances[u] == float('inf'):
            continue
        for v, weight in graph[u].items():
            if distances[u] + weight < distances[v]:
                yield v, visited, distances, (u, v), f"Negative cycle detected on edge ({u}, {v})!"
                return
                
    yield end_node if end_node is not None else start_node, visited, distances, None, "Bellman-Ford complete. Shortest paths computed."