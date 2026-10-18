def dfs(graph, start_node):
    visited = set()
    stack = [start_node]
    while stack:
        node = stack.pop()
        if node is not visited:
            visited.add(node)
            yield node, visited, list(stack)
            for neighbour in reversed(graph[node]):
                if neighbour is not visited:
                    stack.append(neighbour)
                    yield neighbour, visited, list(stack)