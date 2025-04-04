def dfs(maze, start, end, weights):
    """Depth-First Search with weighted nodes and multiple paths"""
    stack = [(start, [start], 0)]  # (position, path, cost)
    visited = set()
    best_path = None
    min_cost = float('inf')
    nodes_expanded = 0

    while stack:
        nodes_expanded += 1
        (x, y), path, cost = stack.pop()
        
        if (x, y) == end:
            if cost < min_cost:
                min_cost = cost
                best_path = path
            continue
        
        if (x, y) in visited:
            continue
        visited.add((x, y))
        
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0:
                new_cost = cost + weights[nx][ny]
                new_path = path + [(nx, ny)]
                stack.append(((nx, ny), new_path, new_cost))
    
    return best_path, nodes_expanded, min_cost if best_path else 0