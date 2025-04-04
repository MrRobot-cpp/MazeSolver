import heapq

def astar(maze, start, end, weights):
    """A* algorithm with weighted nodes and multiple paths"""
    open_set = []
    heapq.heappush(open_set, (0, 0, start, [start]))  # (f_cost, g_cost, position, path)
    visited = {}
    nodes_expanded = 0
    best_path = None
    min_cost = float('inf')

    while open_set:
        nodes_expanded += 1
        f_cost, g_cost, (x, y), path = heapq.heappop(open_set)
        
        if (x, y) == end:
            if g_cost < min_cost:
                min_cost = g_cost
                best_path = path
            continue
        
        if (x, y) in visited and visited[(x, y)] <= g_cost:
            continue
        
        visited[(x, y)] = g_cost
        
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0:
                new_g = g_cost + weights[nx][ny]
                new_f = new_g + heuristic((nx, ny), end)
                new_path = path + [(nx, ny)]
                if (nx, ny) not in visited or new_g < visited.get((nx, ny), float('inf')):
                    heapq.heappush(open_set, (new_f, new_g, (nx, ny), new_path))
    
    return best_path, nodes_expanded, min_cost if best_path else 0

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])