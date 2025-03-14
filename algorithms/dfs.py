from maze import get_maze, start_end

def dfs(maze, start, end):
    stack = [start]
    visited = set([start])
    parent = {}

    while stack:
        x, y = stack.pop()
        if (x, y) == end:
            return reconstruct_path(parent, end)

        for nx, ny in get_neighbors(x, y):
            if is_valid_move(maze, nx, ny) and (nx, ny) not in visited:
                stack.append((nx, ny))
                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)

    return None  # No path found

def get_neighbors(x, y):
    return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

def is_valid_move(maze, x, y):
    size = len(maze)
    return 0 <= x < size and 0 <= y < size and maze[x][y] == 0

def reconstruct_path(parent, end):
    path = []
    while end in parent:
        path.append(end)
        end = parent[end]
    path.append(end)  # Add start position
    return path[::-1]

if __name__ == "__main__":
    maze = get_maze()
    start, end = start_end()
    path = dfs(maze, start, end)
    print("DFS Path:", path)
