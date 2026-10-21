def kruskal(graph):
    nodes = list(graph.keys())
    parent = {n: n for n in nodes}
    rank = {n: 0 for n in nodes}
    
    def find(i):
        if parent[i] == i:
            return i
        parent[i] = find(parent[i])
        return parent[i]
        
    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            if rank[root_i] < rank[root_j]:
                root_i, root_j = root_j, root_i
            parent[root_j] = root_i
            if rank[root_i] == rank[root_j]:
                rank[root_i] += 1
            return True
        return False

    all_edges = []
    seen = set()
    for u in graph:
        for v, w in graph[u].items():
            edge = tuple(sorted((u, v)))
            if edge not in seen:
                seen.add(edge)
                all_edges.append((w, u, v))
    all_edges.sort()
    
    mst_edges = []
    visited = set()
    yield None, visited, mst_edges, None, f"Sorted {len(all_edges)} edges by weight for Kruskal's"
    
    for w, u, v in all_edges:
        if union(u, v):
            mst_edges.append((u, v))
            visited.add(u)
            visited.add(v)
            yield v, visited, mst_edges, (u, v), f"Accepted edge ({u}, {v}) [w={w}] (no cycle)"
        else:
            yield v, visited, mst_edges, (u, v), f"Rejected edge ({u}, {v}) [w={w}] (creates cycle)"
            
    total_w = sum(graph[u][v] for u, v in mst_edges if u in graph and v in graph[u])
    yield None, visited, mst_edges, None, f"Kruskal's MST complete (Total weight: {total_w}, Edges: {len(mst_edges)})"