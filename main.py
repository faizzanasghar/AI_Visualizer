import tkinter as tk
from tkinter import messagebox
import time
from collections import deque
import heapq

# Search Logic 

def DLS(graph, startnode, goal, limit, callback=None):
    if limit >= 0:
        
        parent_map = {startnode: None}
        visited = {startnode}
        stack = [[startnode, 0]]
        
        while stack:
            
            curr_node, curr_depth = stack.pop()
            if callback: 
                
                callback(curr_node, "orange")
            
            if goal == curr_node:
                
                return parent_map
            
            if curr_depth < limit:
                
                for n in reversed(graph.get(curr_node, [])):
                    
                    if n not in visited:
                        
                        visited.add(n)
                        parent_map[n] = curr_node
                        stack.append([n, curr_depth + 1])
                        if callback: 
                            
                            callback(n, "cyan")
    return None

def IDDS(graph, startnode, goal, max_limit, callback=None):
    for limit in range(max_limit):
        
        res = DLS(graph, startnode, goal, limit, callback)
        if res:
            
            return res
    return None

def BiDirectional(startNode, goalNode, graph, callback=None):
    if startNode not in graph or goalNode not in graph:
        
        return None
    
    if startNode == goalNode: 
        
        return {startNode: None}, {goalNode: None}, startNode

    f_q, b_q = deque([startNode]), deque([goalNode])
    f_parent, b_parent = {startNode: None}, {goalNode: None}

    while f_q and b_q:
        
        # Forward Step
        f = f_q.popleft()
        if callback: 
            
            callback(f, "orange")
            
        for n in graph.get(f, []):
            
            if n not in f_parent:
                
                f_parent[n] = f
                f_q.append(n)
                if callback: 
                    
                    callback(n, "cyan")
                if n in b_parent: 
                    
                    return f_parent, b_parent, n
                    
        # Backward Step
        b = b_q.popleft()
        if callback: 
            
            callback(b, "purple")
            
        for n in graph.get(b, []):
            
            if n not in b_parent:
                
                b_parent[n] = b
                b_q.append(n)
                if callback: 
                    
                    callback(n, "magenta")
                if n in f_parent: 
                    
                    return f_parent, b_parent, n
    return None

def ucs(map_data, start, goal, callback=None):
    queue = [(0, start, None)]
    parent_map = {}
    visited_costs = {start: 0}

    while queue:
        
        cost, curr, parent = heapq.heappop(queue)
        
        if curr in parent_map:
            
            continue
            
        parent_map[curr] = parent
        if callback: 
            
            callback(curr, "orange")
            
        if curr == goal: 
            
            return parent_map

        for neighbor in map_data.get(curr, {}):
            
            new_cost = cost + 1 
            if neighbor not in visited_costs or new_cost < visited_costs[neighbor]:
                
                visited_costs[neighbor] = new_cost
                heapq.heappush(queue, (new_cost, neighbor, curr))
                if callback: 
                    
                    callback(neighbor, "cyan")
    return None

# GUI Application

class PathFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("FORT Algo Visualizer 2026")
        self.root.configure(bg="#1e1e2e")
        
        self.grid_size = 15
        self.cell_size = 40
        self.grid_state = {} 
        self.start_node = None
        self.target_node = None
    
        self.directions = [(-1, 0), (0, 1), (1, 0), (1, 1), (0, -1), (-1, -1)]
        
        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        self.colors = {
            "bg": "#1e1e2e", "sidebar": "#252539", "text": "#cdd6f4",
            "S": "#a6e3a1", "T": "#89b4fa", "W": "#f38ba8",
            "BFS": "#fab387", "DFS": "#f9e2af", "UCS": "#94e2d5",
            "DLS": "#cba6f7", "IDD": "#f5c2e7", "Bidi": "#eba0ac"
        }

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, width=self.grid_size*self.cell_size, 
                                height=self.grid_size*self.cell_size, bg="white", 
                                highlightthickness=0, bd=0)
        self.canvas.pack(side=tk.LEFT, padx=20, pady=20)
        self.canvas.bind("<Button-1>", self.on_click)

        self.sidebar = tk.Frame(self.root, bg=self.colors["sidebar"], width=200)
        self.sidebar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Label(self.sidebar, text="ALGORITHMS", font=('Segoe UI', 14, 'bold'), 
                 bg=self.colors["sidebar"], fg=self.colors["text"]).pack(pady=20)

        self.add_btn("Breadth First", self.colors["BFS"], self.exec_bfs)
        self.add_btn("Depth First", self.colors["DFS"], self.exec_dfs)
        self.add_btn("Uniform Cost", self.colors["UCS"], self.exec_ucs)
        self.add_btn("Depth Limited", self.colors["DLS"], lambda: self.exec_dls(15))
        self.add_btn("Iterative Deepening", self.colors["IDD"], self.exec_idds)
        self.add_btn("Bidirectional", self.colors["Bidi"], self.exec_bidi)

        tk.Button(self.sidebar, text="RESET GRID", font=('Segoe UI', 10, 'bold'), 
                  bg="#45475a", fg="white", bd=0, cursor="hand2",
                  command=self.reset).pack(side=tk.BOTTOM, fill=tk.X, pady=20, padx=10)
        
        self.draw_grid()

    def add_btn(self, text, color, cmd):
        btn = tk.Button(self.sidebar, text=text, font=('Segoe UI', 10), 
                        bg=color, fg="#11111b", activebackground="#bac2de",
                        bd=0, pady=8, cursor="hand2", command=cmd)
        btn.pack(fill=tk.X, padx=15, pady=5)

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                x1, y1 = c * self.cell_size, r * self.cell_size
                color = "white"
                txt = ""
                if (r, c) == self.start_node: 
                    color, txt = self.colors["S"], "S"
                elif (r, c) == self.target_node: 
                    color, txt = self.colors["T"], "T"
                elif self.grid_state.get((r, c)) == "-1": 
                    color, txt = self.colors["W"], "-1"
                
                self.canvas.create_rectangle(x1, y1, x1+self.cell_size, y1+self.cell_size, 
                                             fill=color, outline="#e6e9ef")
                if txt: 
                    self.canvas.create_text(x1+20, y1+20, text=txt, font=('Arial', 10, 'bold'))

    def on_click(self, event):
        r, c = event.y // self.cell_size, event.x // self.cell_size
        node = (r, c)
        if not self.start_node: 
            self.start_node = node
        elif not self.target_node and node != self.start_node: 
            self.target_node = node
        elif node != self.start_node and node != self.target_node: 
            self.grid_state[node] = "-1"
        self.draw_grid()

    def visualize_callback(self, node, color):
        if node != self.start_node and node != self.target_node:
            x1, y1 = node[1] * self.cell_size, node[0] * self.cell_size
            self.canvas.create_rectangle(x1, y1, x1+self.cell_size, y1+self.cell_size, 
                                         fill=color, outline="#e6e9ef")
            self.root.update()
            time.sleep(0.01)

    def draw_final_path(self, parent_map, end_from):
        curr = end_from
        while curr in parent_map and parent_map[curr] is not None:
            
            curr = parent_map[curr]
            if curr != self.start_node and curr != self.target_node:
                
                self.visualize_callback(curr, "yellow")
                time.sleep(0.02)

    def get_adj(self):
        adj = {}
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.grid_state.get((r, c)) == "-1": 
                    continue
                neighs = []
                for dr, dc in self.directions:
                    nr, nc = r+dr, c+dc
                    if 0<=nr<self.grid_size and 0<=nc<self.grid_size and self.grid_state.get((nr, nc)) != "-1":
                        neighs.append((nr, nc))
                adj[(r, c)] = neighs
        return adj

    def check_ready(self):
        if not self.start_node or not self.target_node:
            
            messagebox.showwarning("Warning", "Please set Start and Target points!")
            return False
        self.draw_grid()
        return True

    def exec_bfs(self):
        if not self.check_ready(): 
            return
        graph = self.get_adj()
        parent_map = {self.start_node: None}
        queue = deque([self.start_node])
        found = False
        
        while queue:
            
            node = queue.popleft()
            if node == self.target_node: 
                
                found = True
                break
            if node != self.start_node:
                
                self.visualize_callback(node, "#cdd6f4")
            
            for n in graph.get(node, []):
                
                if n not in parent_map:
                    
                    parent_map[n] = node
                    queue.append(n)
                    self.visualize_callback(n, "#94e2d5")
        
        if found:
            
            self.draw_final_path(parent_map, self.target_node)
        else:
            
            messagebox.showerror("Error", "No path found via BFS!")

    def exec_dfs(self):
        if not self.check_ready(): 
            return
        graph = self.get_adj()
        parent_map = {self.start_node: None}
        stack = [self.start_node]
        visited = {self.start_node}
        found = False
        
        while stack:
            
            node = stack.pop()
            if node == self.target_node:
                
                found = True
                break
            if node != self.start_node:
                
                self.visualize_callback(node, "#cdd6f4")
            
            for n in reversed(graph.get(node, [])):
                
                if n not in visited:
                    
                    visited.add(n)
                    parent_map[n] = node
                    stack.append(n)
                    self.visualize_callback(n, "#f9e2af")
        
        if found:
            
            self.draw_final_path(parent_map, self.target_node)
        else:
            
            messagebox.showerror("Error", "No path found via DFS!")

    def exec_ucs(self):
        if not self.check_ready(): 
            return
        graph_weighted = {n: {neigh: 1 for neigh in neighs} for n, neighs in self.get_adj().items()}
        parent_map = ucs(graph_weighted, self.start_node, self.target_node, self.visualize_callback)
        if parent_map:
            
            self.draw_final_path(parent_map, self.target_node)
        else:
            
            messagebox.showerror("Error", "No path found via UCS!")

    def exec_dls(self, limit):
        if not self.check_ready(): 
            return
        parent_map = DLS(self.get_adj(), self.start_node, self.target_node, limit, self.visualize_callback)
        if parent_map:
            
            self.draw_final_path(parent_map, self.target_node)
        else:
            
            messagebox.showwarning("Cut off", f"Target not found within depth {limit}")

    def exec_idds(self):
        if not self.check_ready(): 
            return
        parent_map = IDDS(self.get_adj(), self.start_node, self.target_node, self.grid_size*2, self.visualize_callback)
        if parent_map:            
            self.draw_final_path(parent_map, self.target_node)
        else:            
            messagebox.showerror("Error", "IDDFS failed to find target.")

    def exec_bidi(self):
        if not self.check_ready(): 
            return
        res = BiDirectional(self.start_node, self.target_node, self.get_adj(), self.visualize_callback)
        if res:
            
            f_map, b_map, meet = res
            self.visualize_callback(meet, "yellow")
            
            self.draw_final_path(f_map, meet) 
            curr = meet
            while curr in b_map and b_map[curr] is not None:
                
                curr = b_map[curr]
                if curr != self.target_node:
                    
                    self.visualize_callback(curr, "yellow")
                    time.sleep(0.02)
        else: 
            
            messagebox.showerror("Error", "Bidirectional search failed.")

    def reset(self):
        self.grid_state, self.start_node, self.target_node = {}, None, None
        self.draw_grid()

if __name__ == "__main__":
    root = tk.Tk()
    app = PathFinder(root)
    root.mainloop()