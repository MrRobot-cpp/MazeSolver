import heapq

def astar(maze, start, end, weights):
    """A* for shortest weighted path"""
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, end), 0, start, [start]))
    visited = {}
    nodes_expanded = 0

    while open_set:
        nodes_expanded += 1
        _, g_cost, (x, y), path = heapq.heappop(open_set)
        
        if (x, y) == end:
            return path, nodes_expanded, g_cost
        
        if (x, y) in visited and visited[(x, y)] <= g_cost:
            continue
        
        visited[(x, y)] = g_cost
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0:
                new_g = g_cost + weights[nx][ny]
                heapq.heappush(open_set, (new_g + heuristic((nx, ny), end), new_g, (nx, ny), path + [(nx, ny)]))
    
    return None, nodes_expanded, 0

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])