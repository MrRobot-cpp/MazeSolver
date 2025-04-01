import tkinter as tk
from maze import get_static_maze, generate_random_maze, start_end
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.aStar import astar
import time

CELL_SIZE = 40  # Size of each grid cell

class MazeSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver")

        # Canvas for drawing the maze
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        # Maze type selection
        self.maze_type = tk.StringVar(value="Static")
        tk.Label(root, text="Select Maze Type:").pack()
        tk.Radiobutton(root, text="Static Maze", variable=self.maze_type, value="Static", command=self.load_maze).pack()
        tk.Radiobutton(root, text="Random Maze", variable=self.maze_type, value="Random", command=self.load_maze).pack()

        # Algorithm selection
        self.algorithm_choice = tk.StringVar(value="BFS")  # Default selection
        tk.Label(root, text="Select Algorithm:").pack()
        tk.Radiobutton(root, text="BFS", variable=self.algorithm_choice, value="BFS").pack()
        tk.Radiobutton(root, text="DFS", variable=self.algorithm_choice, value="DFS").pack()
        tk.Radiobutton(root, text="A*", variable=self.algorithm_choice, value="A*").pack()

        # Solve button
        self.solve_button = tk.Button(root, text="Start", command=self.solve_maze)
        self.solve_button.pack()

        # Load initial maze
        self.load_maze()

    def load_maze(self):
        """Loads either the static maze or generates a random one."""
        if self.maze_type.get() == "Static":
            self.maze = get_static_maze()
        else:
            self.maze = generate_random_maze(size=10)  # Adjust size as needed
        self.start, self.end = start_end()
        self.draw_maze()

    def draw_maze(self):
        """Draws the maze on the canvas."""
        self.canvas.delete("all")
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                x0, y0 = j * CELL_SIZE, i * CELL_SIZE
                x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE

                if self.maze[i][j] == 1:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="black")  # Walls
                else:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="gray")

        # Draw start and end points
        sx, sy = self.start
        ex, ey = self.end
        self.canvas.create_rectangle(sy * CELL_SIZE, sx * CELL_SIZE, (sy + 1) * CELL_SIZE, (sx + 1) * CELL_SIZE, fill="green")
        self.canvas.create_rectangle(ey * CELL_SIZE, ex * CELL_SIZE, (ey + 1) * CELL_SIZE, (ex + 1) * CELL_SIZE, fill="red")

    def solve_maze(self):
        """Runs the selected algorithm and visualizes the solution."""
        algo = self.algorithm_choice.get()
        start_time = time.time()
        
        if algo == "BFS":
            path = bfs(self.maze, self.start, self.end)
        elif algo == "DFS":
            path = dfs(self.maze, self.start, self.end)
        elif algo == "A*":
            path = astar(self.maze, self.start, self.end)
        else:
            return  # Invalid selection

        execution_time = time.time() - start_time

        if path:
            for (x, y) in path[1:-1]:  # Exclude start and end points
                self.canvas.create_rectangle(y * CELL_SIZE, x * CELL_SIZE, (y + 1) * CELL_SIZE, (x + 1) * CELL_SIZE, fill="blue")
            print(f"{algo} Execution Time: {execution_time:.6f} seconds")
            print(f"Nodes Expanded: {len(path)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeSolverGUI(root)
    root.mainloop()
