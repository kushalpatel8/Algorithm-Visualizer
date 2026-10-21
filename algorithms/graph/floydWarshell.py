def floyd_warshall(graph):
    nodes = sorted(list(graph.keys()))
    # Initialize distances
    distances = {u: {v: float('inf') for v in nodes} for u in nodes}
    for u in nodes:
        distances[u][u] = 0
        if u in graph:
            for v, weight in graph[u].items():
                distances[u][v] = min(distances[u][v], weight)
                
    visited = set()
    yield None, visited, distances, None, "Initialized distance matrix for Floyd-Warshall"
    
    for k in nodes:
        visited.add(k)
        for i in nodes:
            if distances[i][k] == float('inf'):
                continue
            for j in nodes:
                if distances[k][j] == float('inf'):
                    continue
                new_dist = distances[i][k] + distances[k][j]
                if new_dist < distances[i][j]:
                    distances[i][j] = new_dist
                    yield k, visited, distances, (i, j), f"Pivot {k}: Path {i}->{k}->{j} updated to {new_dist}"
                else:
                    yield k, visited, distances, (i, j), f"Pivot {k}: Checking path {i}->{j} via {k}"
                    
    yield None, visited, distances, None, "Floyd-Warshall complete. All-pairs shortest paths computed."