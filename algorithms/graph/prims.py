import heapq

def prim(graph, start_node=0):
    visited = {start_node}
    mst_edges = []
    edges = []
    
    for neighbor, weight in graph[start_node].items():
        heapq.heappush(edges, (weight, start_node, neighbor))
        
    yield start_node, visited, mst_edges, None, f"Starting Prim's MST from node {start_node}"
    
    while edges and len(visited) < len(graph):
        weight, u, v = heapq.heappop(edges)
        if v in visited:
            continue
            
        visited.add(v)
        mst_edges.append((u, v))
        yield v, visited, mst_edges, (u, v), f"Added edge ({u}, {v}) [w={weight}] to MST"
        
        for neighbor, next_w in graph[v].items():
            if neighbor not in visited:
                heapq.heappush(edges, (next_w, v, neighbor))
                yield neighbor, visited, mst_edges, (v, neighbor), f"Discovered edge ({v}, {neighbor}) [w={next_w}]"
                
    total_w = sum(graph[u][v] for u, v in mst_edges if u in graph and v in graph[u])
    yield None, visited, mst_edges, None, f"Prim's MST complete (Total weight: {total_w}, Edges: {len(mst_edges)})"