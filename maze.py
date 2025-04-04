import random

def get_static_maze():
    """Modified static maze with multiple paths"""
    return [
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [1, 1, 0, 1, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    ]

def generate_random_maze(size=10):
    """Generates maze with multiple paths using Prim's algorithm"""
    maze = [[1] * size for _ in range(size)]
    frontiers = []
    start = (0, 0)
    end = (size-1, size-1)
    
    # Initialize with start point
    maze[start[0]][start[1]] = 0
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = start[0]+dx, start[1]+dy
        if 0 <= nx < size and 0 <= ny < size:
            frontiers.append((nx, ny, start[0], start[1]))
    
    # Create multiple paths
    while frontiers:
        x, y, px, py = frontiers.pop(random.randint(0, len(frontiers)-1))
        if maze[x][y] == 1:
            maze[x][y] = 0
            maze[(x + px) // 2][(y + py) // 2] = 0
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < size and 0 <= ny < size:
                    frontiers.append((nx, ny, x, y))
    
    # Ensure end is open and multiple paths exist
    maze[end[0]][end[1]] = 0
    for dx, dy in [(-1,0),(0,-1)]:
        nx, ny = end[0]+dx, end[1]+dy
        if 0 <= nx < size and 0 <= ny < size:
            maze[nx][ny] = 0
    
    return maze