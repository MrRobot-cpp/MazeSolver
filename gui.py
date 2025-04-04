import tkinter as tk
from tkinter import ttk
from maze import get_static_maze, generate_random_maze
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.aStar import astar
import time
import random

class MazeSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver")
        
        # Configuration
        self.maze_size = tk.IntVar(value=10)
        self.wall_density = tk.DoubleVar(value=0.3)
        self.cell_size = 40
        
        # Initialize maze
        self.maze = None
        self.weights = None
        self.start = (0, 0)
        self.end = None
        self.solution_path = None
        
        self.setup_ui()
        self.load_maze()
    
    def setup_ui(self):
        """Initialize all UI components"""
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Maze controls
        tk.Label(control_frame, text="Maze Size:").grid(row=0, column=0, sticky="w")
        tk.Spinbox(control_frame, from_=5, to=50, textvariable=self.maze_size, 
                  width=5, command=self.update_maze_size).grid(row=0, column=1)
        
        tk.Label(control_frame, text="Wall Density:").grid(row=0, column=2, sticky="w")
        tk.Scale(control_frame, from_=0.1, to=0.5, resolution=0.05, orient=tk.HORIZONTAL,
                variable=self.wall_density, length=150).grid(row=0, column=3)
        
        tk.Label(control_frame, text="Maze Type:").grid(row=1, column=0, sticky="w")
        self.maze_type = tk.StringVar(value="Static")
        tk.Radiobutton(control_frame, text="Static", variable=self.maze_type, 
                      value="Static", command=self.load_maze).grid(row=1, column=1)
        tk.Radiobutton(control_frame, text="Random", variable=self.maze_type, 
                      value="Random", command=self.load_maze).grid(row=1, column=2)
        
        # Algorithm selection
        tk.Label(control_frame, text="Algorithm:").grid(row=2, column=0, sticky="w")
        self.algorithm_choice = tk.StringVar(value="BFS")
        algorithms = ["BFS", "DFS", "A*"]
        for i, algo in enumerate(algorithms, 1):
            tk.Radiobutton(control_frame, text=algo, variable=self.algorithm_choice, 
                          value=algo).grid(row=2, column=i)
        
        # Action buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        tk.Button(button_frame, text="Solve", command=self.solve_maze).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Clear Solution", command=self.clear_solution).pack(side=tk.LEFT)
        tk.Button(button_frame, text="New Maze", command=self.load_maze).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Compare All", command=self.compare_algorithms).pack(side=tk.LEFT)
        
        # Canvas for maze display
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Performance display
        self.perf_label = tk.Label(self.root, text="Ready to solve!", 
                                 justify=tk.LEFT, relief=tk.SUNKEN, padx=5, pady=5)
        self.perf_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_maze_size(self):
        """Adjust display based on maze size"""
        size = self.maze_size.get()
        self.cell_size = min(40, 800 // size)  # Prevent too large cells
        self.load_maze()
    
    def load_maze(self):
        """Generate new maze with current settings"""
        size = self.maze_size.get()
        self.end = (size-1, size-1)
        
        if self.maze_type.get() == "Static":
            self.maze = get_static_maze(size)
        else:
            self.maze = generate_random_maze(size, self.wall_density.get())
        
        # Assign random weights (1-3) to paths
        self.weights = [[random.randint(1, 3) if cell == 0 else 0 
                        for cell in row] for row in self.maze]
        
        self.solution_path = None
        self.draw_maze()
        self.perf_label.config(text=f"New {size}x{size} maze generated")
    
    def draw_maze(self):
        """Visualize the maze"""
        self.canvas.delete("all")
        size = len(self.maze)
        canvas_size = size * self.cell_size
        self.canvas.config(width=canvas_size, height=canvas_size)
        
        for i in range(size):
            for j in range(size):
                x0, y0 = j * self.cell_size, i * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size

                if self.maze[i][j] == 1:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="black")
                else:
                    intensity = 255 - (self.weights[i][j] * 50)
                    color = f"#{intensity:02x}{intensity:02x}ff"
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="gray")
                    if self.cell_size > 20:  # Only show text if space allows
                        self.canvas.create_text((x0+x1)//2, (y0+y1)//2, 
                                              text=str(self.weights[i][j]))

        # Mark start (green) and end (red)
        self.canvas.create_rectangle(0, 0, self.cell_size, self.cell_size, fill="green")
        self.canvas.create_rectangle(
            (size-1)*self.cell_size, (size-1)*self.cell_size,
            size*self.cell_size, size*self.cell_size, 
            fill="red"
        )
        
        if self.solution_path:
            self.draw_solution(self.solution_path)
    
    def draw_solution(self, path):
        """Draw the solution path in blue"""
        for (x, y) in path[1:-1]:  # Skip start and end points
            self.canvas.create_rectangle(
                y * self.cell_size, x * self.cell_size,
                (y + 1) * self.cell_size, (x + 1) * self.cell_size,
                fill="blue"
            )
    
    def solve_maze(self):
        """Run selected algorithm with precise timing"""
        algo = self.algorithm_choice.get()
        
        # Warm-up run (for accurate timing)
        if algo == "BFS":
            bfs(self.maze, self.start, self.end)
        elif algo == "DFS":
            dfs(self.maze, self.start, self.end)
        elif algo == "A*":
            astar(self.maze, self.start, self.end, self.weights)
        
        # Timed execution
        start_time = time.perf_counter()
        
        if algo == "BFS":
            path, nodes, cost = bfs(self.maze, self.start, self.end)
        elif algo == "DFS":
            path, nodes, cost = dfs(self.maze, self.start, self.end)
        elif algo == "A*":
            path, nodes, cost = astar(self.maze, self.start, self.end, self.weights)
        
        elapsed = time.perf_counter() - start_time
        
        if not path:
            self.perf_label.config(text=f"{algo}: No solution found!")
            return
            
        self.solution_path = path
        self.draw_maze()
        
        self.perf_label.config(text=(
            f"{algo} Results:\n"
            f"Time: {elapsed:.6f} seconds\n"
            f"Path Length: {len(path)} steps\n"
            f"Nodes Expanded: {nodes}\n"
            f"Total Cost: {cost}"
        ))
    
    def clear_solution(self):
        """Reset the solution display"""
        self.solution_path = None
        self.draw_maze()
        self.perf_label.config(text="Solution cleared")
    
    def compare_algorithms(self):
        """Compare all three algorithms"""
        results = []
        size = len(self.maze)
        
        for algo in ["BFS", "DFS", "A*"]:
            # Warm-up
            if algo == "BFS":
                bfs(self.maze, self.start, self.end)
            elif algo == "DFS":
                dfs(self.maze, self.start, self.end)
            elif algo == "A*":
                astar(self.maze, self.start, self.end, self.weights)
            
            # Timed run
            start_time = time.perf_counter()
            
            if algo == "BFS":
                path, nodes, cost = bfs(self.maze, self.start, self.end)
            elif algo == "DFS":
                path, nodes, cost = dfs(self.maze, self.start, self.end)
            elif algo == "A*":
                path, nodes, cost = astar(self.maze, self.start, self.end, self.weights)
            
            elapsed = time.perf_counter() - start_time
            
            results.append((
                algo,
                elapsed,
                len(path) if path else 0,
                nodes,
                cost if path else 0
            ))
        
        # Format results
        comparison = (
            f"Algorithm Comparison ({size}x{size} maze):\n"
            "Algorithm   Time (s)       Path Length  Nodes Expanded  Total Cost\n"
            "---------------------------------------------------------------\n"
        )
        
        for algo, time_taken, path_len, nodes, cost in results:
            comparison += f"{algo:<8} {time_taken:>10.6f}  {path_len:>12}  {nodes:>14}  {cost:>10}\n"
        
        self.perf_label.config(text=comparison)

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeSolverGUI(root)
    root.mainloop()