import random

def get_static_maze(size=10):
    """Returns a predefined maze (0=path, 1=wall) with adjustable size"""
    base_maze = [
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
    
    # Scale the maze if size is different
    if size != 10:
        scaled_maze = []
        for i in range(size):
            row = []
            for j in range(size):
                row.append(base_maze[i*10//size][j*10//size])
            scaled_maze.append(row)
        return scaled_maze
    return base_maze

def generate_random_maze(size=10, wall_prob=0.3):
    """Generates a random maze with adjustable size and wall density"""
    maze = [[0 if random.random() > wall_prob else 1 for _ in range(size)] for _ in range(size)]
    maze[0][0] = 0  # Ensure start is open
    maze[size-1][size-1] = 0  # Ensure end is open
    
    # Ensure there's at least one path
    for i in range(1, size):
        maze[0][i] = 0  # Open first row
        maze[i][size-1] = 0  # Open last column
    
    return maze