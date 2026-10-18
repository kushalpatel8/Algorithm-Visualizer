import heapq

def dijkstra(graph, start_node, end_node):
    dists = {node : float('inf') for node in graph}
    dists[start_node] = 0
    pq = [(0, start_node)]
    visited = set()
    while pq:
        curr_dist , curr_node = heapq.heappop()
        if curr_node in visited:
            continue
        visited.add(curr_node)
        yield curr_node, visited, dists
        if curr_node == end_node:
            break
        
        for neighbour, wt in graph[curr_node].items():
            dist = curr_dist + wt
            if dist < dists[neighbour]:
                dists[neighbour] = dist
                heapq.heappush(pq, (dist, neighbour))
                yield neighbour, visited, dists
            