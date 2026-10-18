import heapq

def a_star(graph, start_node, end_node, heuristic):
    # heuristic is a dict {node: h_value}
    pq = [(heuristic[start_node], 0, start_node)]
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0
    visited = set()
    
    while pq:
        f_score, g_score, current_node = heapq.heappop(pq)
        if current_node in visited:
            continue
        visited.add(current_node)
        yield current_node, visited, distances
        
        if current_node == end_node:
            break
            
        for neighbor, weight in graph[current_node].items():
            tentative_g_score = g_score + weight
            if tentative_g_score < distances[neighbor]:
                distances[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic[neighbor]
                heapq.heappush(pq, (f_score, tentative_g_score, neighbor))
                yield neighbor, visited, distances