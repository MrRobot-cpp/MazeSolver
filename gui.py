import tkinter as tk
from tkinter import ttk
from maze import get_static_maze, generate_random_maze
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.aStar import astar
import time
import random  # Add this import

CELL_SIZE = 40  # Size of each grid cell

class MazeSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver")
        
        # Initialize maze-related attributes
        self.maze = None
        self.weights = None
        self.start = (0, 0)
        self.end = (9, 9)
        
        # Control frame
        control_frame = tk.Frame(root)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Canvas for drawing the maze
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()
        
        # Maze controls
        tk.Label(control_frame, text="Maze Type:").grid(row=0, column=0, sticky="w")
        self.maze_type = tk.StringVar(value="Static")
        tk.Radiobutton(control_frame, text="Static", variable=self.maze_type, 
                      value="Static", command=self.load_maze).grid(row=0, column=1)
        tk.Radiobutton(control_frame, text="Random", variable=self.maze_type, 
                      value="Random", command=self.load_maze).grid(row=0, column=2)
        
        # Algorithm selection
        tk.Label(control_frame, text="Algorithm:").grid(row=1, column=0, sticky="w")
        self.algorithm_choice = tk.StringVar(value="BFS")
        algorithms = ["BFS", "DFS", "A*"]
        for i, algo in enumerate(algorithms, 1):
            tk.Radiobutton(control_frame, text=algo, variable=self.algorithm_choice, 
                          value=algo).grid(row=1, column=i)
        
        # Buttons
        tk.Button(control_frame, text="Solve", command=self.solve_maze).grid(row=2, column=0)
        tk.Button(control_frame, text="Compare All", command=self.compare_algorithms).grid(row=2, column=1)
        tk.Button(control_frame, text="New Maze", command=self.load_maze).grid(row=2, column=2)
        
        # Performance label
        self.perf_label = tk.Label(root, text="", justify=tk.LEFT)
        self.perf_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load initial maze
        self.load_maze()

    def load_maze(self):
        """Loads the selected maze type with weights"""
        if self.maze_type.get() == "Static":
            self.maze = get_static_maze()
        else:
            self.maze = generate_random_maze()
        
        # Generate weights (1-3 for all paths)
        self.weights = [[1 if cell == 0 else 0 for cell in row] for row in self.maze]
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                if self.maze[i][j] == 0:
                    self.weights[i][j] = random.randint(1, 3)
        
        self.draw_maze()

    def draw_maze(self):
        """Draws the maze with weights on the canvas."""
        self.canvas.delete("all")
        size = len(self.maze)
        canvas_size = size * CELL_SIZE
        self.canvas.config(width=canvas_size, height=canvas_size)
        
        for i in range(size):
            for j in range(size):
                x0, y0 = j * CELL_SIZE, i * CELL_SIZE
                x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE

                if self.maze[i][j] == 1:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="black")
                else:
                    # Color based on weight (lighter = lower cost)
                    intensity = 255 - (self.weights[i][j] * 50)
                    color = f"#{intensity:02x}{intensity:02x}ff"
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="gray")
                    self.canvas.create_text((x0+x1)//2, (y0+y1)//2, 
                                          text=str(self.weights[i][j]))

        # Draw start and end points
        sx, sy = self.start
        ex, ey = self.end
        self.canvas.create_rectangle(sy * CELL_SIZE, sx * CELL_SIZE, 
                                   (sy + 1) * CELL_SIZE, (sx + 1) * CELL_SIZE, fill="green")
        self.canvas.create_rectangle(ey * CELL_SIZE, ex * CELL_SIZE, 
                                   (ey + 1) * CELL_SIZE, (ex + 1) * CELL_SIZE, fill="red")

    def solve_maze(self):
        """Runs the selected algorithm and visualizes the solution."""
        algo = self.algorithm_choice.get()
        self.run_algorithm(algo)

    def compare_algorithms(self):
        """Compares all three algorithms on the current maze."""
        results = []
        for algo in ["BFS", "DFS", "A*"]:
            results.append(self.run_algorithm(algo, compare_mode=True))
        
        comparison_text = "Algorithm Comparison:\n"
        for algo, time_taken, path_len, nodes_expanded, total_cost in results:
            comparison_text += (f"{algo}: Time={time_taken:.4f}s, Path={path_len}, "
                             f"Nodes={nodes_expanded}, Cost={total_cost}\n")
        
        self.perf_label.config(text=comparison_text)

    def run_algorithm(self, algo, compare_mode=False):
        """Runs a specific algorithm and returns performance metrics."""
        start_time = time.time()
        
        if algo == "BFS":
            path, nodes_expanded, total_cost = bfs(self.maze, self.start, self.end, self.weights)
        elif algo == "DFS":
            path, nodes_expanded, total_cost = dfs(self.maze, self.start, self.end, self.weights)
        elif algo == "A*":
            path, nodes_expanded, total_cost = astar(self.maze, self.start, self.end, self.weights)
        else:
            return None
        
        execution_time = time.time() - start_time

        if not path:
            if not compare_mode:
                self.perf_label.config(text=f"{algo}: No solution found!")
            return (algo, execution_time, 0, nodes_expanded, 0)

        if not compare_mode:
            self.draw_solution(path)
            perf_text = (f"{algo} Performance:\n"
                       f"Time: {execution_time:.4f} seconds\n"
                       f"Path Length: {len(path)}\n"
                       f"Nodes Expanded: {nodes_expanded}\n"
                       f"Total Cost: {total_cost}")
            self.perf_label.config(text=perf_text)
        
        return (algo, execution_time, len(path), nodes_expanded, total_cost)

    def draw_solution(self, path):
        """Draws the solution path all at once."""
        for (x, y) in path[1:-1]:  # Exclude start and end points
            self.canvas.create_rectangle(y * CELL_SIZE, x * CELL_SIZE,
                                      (y + 1) * CELL_SIZE, (x + 1) * CELL_SIZE,
                                      fill="blue")

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeSolverGUI(root)
    root.mainloop()