from ui.controls import ControlPanel
from ui.styles import apply_mpl_theme, get_mpl_palette
import random
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel
from PySide6.QtCore import QTimer, Qt

from algorithms.graph.aStar import a_star
from algorithms.graph.bellmonFord import bellman_ford
from algorithms.graph.bfs import bfs
from algorithms.graph.dfs import dfs
from algorithms.graph.dijkstra import dijkstra
from algorithms.graph.floydWarshell import floyd_warshall
from algorithms.graph.prims import prim
from algorithms.graph.kruskull import kruskal

class GraphVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        
        # Algorithm Selector
        layout.addWidget(QLabel("Select Graph Algorithm:"))
        self.algo_selector = QComboBox()
        self.algo_selector.addItems([
            "BFS", 
            "DFS", 
            "Dijkstra", 
            "A* Search",
            "Bellman-Ford",
            "Floyd-Warshall",
            "Prim's Algorithm",
            "Kruskal's Algorithm"
        ])
        layout.addWidget(self.algo_selector)
        
        # Complexity Info Badge
        self.complexity_label = QLabel()
        self.complexity_label.setObjectName("complexity_badge")
        layout.addWidget(self.complexity_label)
        self.algo_selector.currentTextChanged.connect(self.update_complexity_info)
        
        # Status Label
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("status_banner")
        layout.addWidget(self.status_label)
        
        self.update_complexity_info()
        
        # Matplotlib Figure with dynamic theme
        self.figure, self.ax = plt.subplots(figsize=(8, 4.5))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # Control Panel
        self.controls = ControlPanel()
        layout.addWidget(self.controls)
        
        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_step)
        self.generator = None
        self.speed = 50
        
        # Data
        self.graph = {}
        self.weighted_graph = {}
        self.nx_graph = nx.Graph()
        self.pos = {}
        self.reset_data()
        
        # Connections
        self.controls.play_clicked.connect(self.start_animation)
        self.controls.pause_clicked.connect(self.pause_animation)
        self.controls.step_clicked.connect(self.single_step)
        self.controls.reset_clicked.connect(self.reset_data)
        self.controls.speed_changed.connect(self.set_speed)

    def update_theme(self):
        self.draw_graph()

    def reset_data(self):
        self.pause_animation()
        while True:
            g = nx.gnm_random_graph(8, 12)
            if nx.is_connected(g):
                self.nx_graph = g
                break
        self.pos = nx.spring_layout(self.nx_graph, seed=42)
        
        self.graph = {n: list(self.nx_graph.neighbors(n)) for n in self.nx_graph.nodes()}
        
        self.weighted_graph = {n: {} for n in self.nx_graph.nodes()}
        for u, v in self.nx_graph.edges():
            w = random.randint(1, 9)
            self.weighted_graph[u][v] = w
            self.weighted_graph[v][u] = w
        
        target = max(self.nx_graph.nodes())
        self.target_node = target
        self.heuristic = {n: random.randint(1, 8) for n in self.nx_graph.nodes()}
        self.heuristic[target] = 0
        
        self.status_label.setText(f"Graph initialized ({len(self.nx_graph.nodes())} nodes, {len(self.nx_graph.edges())} edges). Target node: {target}")
        self.draw_graph()
        self.generator = None

    def draw_graph(self, current_node=None, visited=set(), active_edge=None, mst_edges=None, status_msg=""):
        self.ax.clear()
        apply_mpl_theme(self.figure, self.ax)
        p = get_mpl_palette()
        
        node_colors = []
        for n in self.nx_graph.nodes():
            if n == current_node:
                node_colors.append(p['highlight'])
            elif n in visited:
                node_colors.append(p['success'])
            else:
                node_colors.append(p['primary'])
        
        edge_colors = []
        edge_widths = []
        for u, v in self.nx_graph.edges():
            if active_edge and ((u, v) == active_edge or (v, u) == active_edge):
                edge_colors.append(p['highlight'])
                edge_widths.append(3.5)
            elif mst_edges and ((u, v) in mst_edges or (v, u) in mst_edges):
                edge_colors.append(p['primary'])
                edge_widths.append(3.0)
            else:
                edge_colors.append(p['inactive'])
                edge_widths.append(1.8)
        
        nx.draw_networkx_nodes(self.nx_graph, self.pos, ax=self.ax, node_color=node_colors, node_size=650)
        nx.draw_networkx_labels(self.nx_graph, self.pos, ax=self.ax, font_color='#ffffff', font_weight='bold', font_size=11)
        nx.draw_networkx_edges(self.nx_graph, self.pos, ax=self.ax, edge_color=edge_colors, width=edge_widths)
        
        algo_name = self.algo_selector.currentText()
        if algo_name in ["Dijkstra", "A* Search", "Bellman-Ford", "Floyd-Warshall", "Prim's Algorithm", "Kruskal's Algorithm"]:
            edge_labels = {(u, v): self.weighted_graph[u][v] for u, v in self.nx_graph.edges() if u in self.weighted_graph and v in self.weighted_graph[u]}
            nx.draw_networkx_edge_labels(self.nx_graph, self.pos, edge_labels=edge_labels, ax=self.ax, 
                                         font_size=9, font_color=p['text'], 
                                         bbox=dict(facecolor=p['ax_bg'], edgecolor=p['border'], boxstyle='round,pad=0.2'))
            
        self.ax.axis('off')
        if status_msg:
            self.status_label.setText(status_msg)
        self.figure.tight_layout()
        self.canvas.draw()

    def init_generator(self):
        algo_name = self.algo_selector.currentText()
        target = getattr(self, 'target_node', max(self.nx_graph.nodes()))
        if algo_name == "BFS":
            self.generator = bfs(self.graph, 0)
        elif algo_name == "DFS":
            self.generator = dfs(self.graph, 0)
        elif algo_name == "Dijkstra":
            self.generator = dijkstra(self.weighted_graph, 0, target)
        elif algo_name == "A* Search":
            self.generator = a_star(self.weighted_graph, 0, target, self.heuristic)
        elif algo_name == "Bellman-Ford":
            self.generator = bellman_ford(self.weighted_graph, 0, target)
        elif algo_name == "Floyd-Warshall":
            self.generator = floyd_warshall(self.weighted_graph)
        elif algo_name == "Prim's Algorithm":
            self.generator = prim(self.weighted_graph, 0)
        elif algo_name == "Kruskal's Algorithm":
            self.generator = kruskal(self.weighted_graph)

    def start_animation(self):
        if not self.generator:
            self.init_generator()
        self.timer.start(101 - self.speed)

    def pause_animation(self):
        self.timer.stop()

    def single_step(self):
        self.pause_animation()
        if not self.generator:
            self.init_generator()
        self.next_step()

    def set_speed(self, value):
        self.speed = value
        if self.timer.isActive():
            self.timer.start(101 - self.speed)

    def next_step(self):
        try:
            res = next(self.generator)
            node = res[0]
            visited = res[1] if len(res) > 1 and isinstance(res[1], (set, list)) else set()
            active_edge = None
            mst_edges = None
            status_msg = ""
            
            algo_name = self.algo_selector.currentText()
            if algo_name in ["Bellman-Ford", "Floyd-Warshall"]:
                if len(res) >= 4:
                    active_edge = res[3]
                if len(res) >= 5:
                    status_msg = res[4]
            elif algo_name in ["Prim's Algorithm", "Kruskal's Algorithm"]:
                if len(res) >= 3 and isinstance(res[2], list):
                    mst_edges = res[2]
                if len(res) >= 4:
                    active_edge = res[3]
                if len(res) >= 5:
                    status_msg = res[4]
            elif algo_name in ["Dijkstra", "A* Search"]:
                if len(res) >= 3 and isinstance(res[2], dict):
                    if node is not None and node in res[2]:
                        cost = res[2][node]
                        status_msg = f"Visiting Node {node} (Distance: {cost if cost != float('inf') else '∞'})"
            elif algo_name in ["BFS", "DFS"]:
                structure_name = "Queue" if algo_name == "BFS" else "Stack"
                if len(res) >= 3 and isinstance(res[2], list):
                    status_msg = f"Current Node {node} | {structure_name}: {res[2]}"
                    
            self.draw_graph(node, visited, active_edge=active_edge, mst_edges=mst_edges, status_msg=status_msg)
        except StopIteration:
            self.timer.stop()
            self.generator = None
            self.status_label.setText("🎉 Graph algorithm execution completed!")

    def update_complexity_info(self, algo_name=None):
        if not algo_name:
            algo_name = self.algo_selector.currentText()
        complexities = {
            "BFS": {"time": "O(V + E)", "space": "O(V)", "note": "Unweighted shortest paths & traversal"},
            "DFS": {"time": "O(V + E)", "space": "O(V)", "note": "Traversal & cycle detection"},
            "Dijkstra": {"time": "O((V + E) log V)", "space": "O(V)", "note": "Weighted shortest paths (non-negative)"},
            "A* Search": {"time": "O(E)", "space": "O(V)", "note": "Heuristic pathfinding"},
            "Bellman-Ford": {"time": "O(V · E)", "space": "O(V)", "note": "Shortest path with negative weights/cycles"},
            "Floyd-Warshall": {"time": "O(V³)", "space": "O(V²)", "note": "All-pairs shortest paths"},
            "Prim's Algorithm": {"time": "O((V + E) log V)", "space": "O(V)", "note": "Minimum Spanning Tree (MST)"},
            "Kruskal's Algorithm": {"time": "O(E log E)", "space": "O(V)", "note": "Minimum Spanning Tree (MST)"},
        }
        info = complexities.get(algo_name, {"time": "N/A", "space": "N/A", "note": ""})
        p = get_mpl_palette()
        self.complexity_label.setText(
            f"⏱ <b>Time Complexity:</b> <span style='color:{p['primary']}'>{info['time']}</span> &nbsp;|&nbsp; "
            f"💾 <b>Space:</b> <span style='color:{p['success']}'>{info['space']}</span> &nbsp;|&nbsp; "
            f"📌 <i><span style='color:{p['text']}'>{info['note']}</span></i>"
        )