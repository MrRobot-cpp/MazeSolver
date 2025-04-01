import random

def get_static_maze():
    return [
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0, 1, 1, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
    ]

def generate_random_maze(size=10):
    maze = [[1] * size for _ in range(size)]  # Start with all walls
    
    def carve_path(x, y):
        """Recursive DFS to carve a valid path."""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2  # Move two steps at a time
            if 0 <= nx < size and 0 <= ny < size and maze[nx][ny] == 1:
                maze[x + dx][y + dy] = 0  # Open wall in between
                maze[nx][ny] = 0  # Open new cell
                carve_path(nx, ny)
    
    # Start maze generation
    maze[0][0] = 0  # Start point
    carve_path(0, 0)
    
    # Ensure exit is open
    end_x, end_y = size - 1, size - 1
    maze[end_x][end_y] = 0
    if maze[end_x - 1][end_y] == 1 and maze[end_x][end_y - 1] == 1:
        maze[end_x - 1][end_y] = 0  # Ensure an open path to the end
    
    return maze

def start_end():
    return (0, 0), (9, 9)
