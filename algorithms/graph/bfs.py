import collections

def bfs(graph, start_node):
    visited = set()
    queue = collections.deque([start_node])
    visited.add(start_node)
    while queue:
        node = queue.popleft()
        yield node, visited, list(queue)
        for neighbour in graph[node]:
            if neighbour is not visited:
                visited.add(neighbour)
                queue.append(neighbour)
                yield neighbour, visited, list(queue)