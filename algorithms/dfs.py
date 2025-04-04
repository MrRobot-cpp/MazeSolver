def dfs(maze, start, end):
    """DFS for pathfinding (not optimal)"""
    stack = [(start, [start])]
    visited = set()
    nodes_expanded = 0

    while stack:
        nodes_expanded += 1
        (x, y), path = stack.pop()
        
        if (x, y) == end:
            return path, nodes_expanded, len(path) - 1
        
        if (x, y) in visited:
            continue
        visited.add((x, y))
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0:
                stack.append(((nx, ny), path + [(nx, ny)]))
    
    return None, nodes_expanded, 0