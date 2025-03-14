import tkinter as tk
from maze import get_maze, start_end
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.aStar import astar

CELL_SIZE = 40  # Size of each grid cell

class MazeSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver")

        # Canvas for drawing the maze
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        # Radio buttons for algorithm selection
        self.algorithm_choice = tk.StringVar(value="BFS")  # Default selection
        tk.Label(root, text="Select Algorithm:").pack()

        tk.Radiobutton(root, text="BFS", variable=self.algorithm_choice, value="BFS").pack()
        tk.Radiobutton(root, text="DFS", variable=self.algorithm_choice, value="DFS").pack()
        tk.Radiobutton(root, text="A*", variable=self.algorithm_choice, value="A*").pack()

        # Start button to run the selected algorithm
        self.solve_button = tk.Button(root, text="Start", command=self.solve_maze)
        self.solve_button.pack()

        # Load maze and start/end positions
        self.maze = get_maze()
        self.start, self.end = start_end()
        self.draw_maze()

    def draw_maze(self):
        """Draws the maze on the canvas."""
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
        if algo == "BFS":
            path = bfs(self.maze, self.start, self.end)
        elif algo == "DFS":
            path = dfs(self.maze, self.start, self.end)
        elif algo == "A*":
            path = astar(self.maze, self.start, self.end)
        else:
            return  # Invalid selection

        if path:
            for (x, y) in path[1:-1]:  # Exclude start and end points
                self.canvas.create_rectangle(y * CELL_SIZE, x * CELL_SIZE, (y + 1) * CELL_SIZE, (x + 1) * CELL_SIZE, fill="blue")

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeSolverGUI(root)
    root.mainloop()
