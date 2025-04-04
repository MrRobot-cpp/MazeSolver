from collections import deque

def bfs(maze, start, end, weights=None):
    """Breadth-First Search with weights and nodes expanded tracking"""
    if weights is None:
        weights = [[1 for _ in row] for row in maze]
    
    queue = deque([(start, [start], 0)])  # (position, path, cost)
    visited = set([start])
    best_path = None
    min_cost = float('inf')
    nodes_expanded = 0

    while queue:
        nodes_expanded += 1
        (x, y), path, cost = queue.popleft()
        
        if (x, y) == end:
            if cost < min_cost:
                min_cost = cost
                best_path = path
            continue
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0 and (nx, ny) not in visited:
                new_cost = cost + weights[nx][ny]
                new_path = path + [(nx, ny)]
                visited.add((nx, ny))
                queue.append(((nx, ny), new_path, new_cost))
    
    return best_path, nodes_expanded, min_cost if best_path else 0

def reconstruct_path(parent, end):
    """Reconstructs path from parent pointers"""
    path = []
    while end in parent:
        path.append(end)
        end = parent[end]
    path.append(end)
    return path[::-1]