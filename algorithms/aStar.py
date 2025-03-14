import heapq
from maze import get_maze, start_end

def astar(maze, start, end):
    open_set = []
    heapq.heappush(open_set, (0, start))
    parent = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            return reconstruct_path(parent, end)

        for neighbor in get_neighbors(*current):
            if not is_valid_move(maze, *neighbor):
                continue

            temp_g_score = g_score[current] + 1
            if neighbor not in g_score or temp_g_score < g_score[neighbor]:
                parent[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor, end)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # No path found

def heuristic(a, b):
    """Heuristic function: Manhattan distance"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

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
    path = astar(maze, start, end)
    print("A* Path:", path)
