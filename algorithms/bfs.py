from collections import deque

def bfs(maze, start, end):
    """BFS for shortest path (unweighted)"""
    queue = deque([(start, [start])])
    visited = set([start])
    nodes_expanded = 0

    while queue:
        nodes_expanded += 1
        (x, y), path = queue.popleft()
        
        if (x, y) == end:
            return path, nodes_expanded, len(path) - 1
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))
    
    return None, nodes_expanded, 0