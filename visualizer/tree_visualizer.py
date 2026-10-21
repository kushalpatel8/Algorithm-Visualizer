from algorithms.tree.tree import postorder, inorder, preorder
from ui.controls import ControlPanel
from ui.styles import apply_mpl_theme, get_mpl_palette

import random
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel
from PySide6.QtCore import QTimer, Qt

class TreeVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        
        # Algorithm Selector
        layout.addWidget(QLabel("Select Tree Traversal:"))
        self.algo_selector = QComboBox()
        self.algo_selector.addItems(["Inorder", "Preorder", "Postorder"])
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
        self.root = None
        self.nodes = []
        self.reset_data()
        
        # Connections
        self.controls.play_clicked.connect(self.start_animation)
        self.controls.pause_clicked.connect(self.pause_animation)
        self.controls.step_clicked.connect(self.single_step)
        self.controls.reset_clicked.connect(self.reset_data)
        self.controls.speed_changed.connect(self.set_speed)

    def update_theme(self):
        self.draw_tree()

    def reset_data(self):
        self.pause_animation()
        self.root = None
        self.nodes = random.sample(range(1, 100), 9)
        for val in self.nodes:
            self.root = self._insert(self.root, val)
        self.status_label.setText(f"BST initialized with {len(self.nodes)} random keys: {self.nodes}")
        self.draw_tree()
        self.generator = None

    def _insert(self, root, val):
        if root is None: return Node(val)
        if val < root.val: root.left = self._insert(root.left, val)
        else: root.right = self._insert(root.right, val)
        return root

    def get_pos(self, node, x=0, y=0, pos=None, layer=1):
        if pos is None:
            pos = {}
        if node:
            pos[node.val] = (x, -y)
            self.get_pos(node.left, x - 1 / 2**layer, y + 1, pos, layer + 1)
            self.get_pos(node.right, x + 1 / 2**layer, y + 1, pos, layer + 1)
        return pos

    def draw_tree(self, current_val=None, visited=[]):
        self.ax.clear()
        apply_mpl_theme(self.figure, self.ax)
        p = get_mpl_palette()
        if not self.root: 
            self.canvas.draw()
            return
        
        G = nx.Graph()
        pos = self.get_pos(self.root)
        
        def add_edges(node):
            if node.left:
                G.add_edge(node.val, node.left.val)
                add_edges(node.left)
            if node.right:
                G.add_edge(node.val, node.right.val)
                add_edges(node.right)
        
        add_edges(self.root)
        
        node_colors = []
        for n in G.nodes():
            if n == current_val:
                node_colors.append(p['highlight'])
            elif n in visited:
                node_colors.append(p['success'])
            else:
                node_colors.append(p['primary'])
        
        nx.draw_networkx_nodes(G, pos, ax=self.ax, node_color=node_colors, node_size=650)
        nx.draw_networkx_labels(G, pos, ax=self.ax, font_color='#ffffff', font_weight='bold', font_size=10)
        nx.draw_networkx_edges(G, pos, ax=self.ax, edge_color=p['border'], width=2.0)
        
        self.ax.axis('off')
        self.figure.tight_layout()
        self.canvas.draw()

    def init_generator(self):
        algo_name = self.algo_selector.currentText()
        if algo_name == "Inorder":
            self.generator = inorder(self.root)
        elif algo_name == "Preorder":
            self.generator = preorder(self.root)
        elif algo_name == "Postorder":
            self.generator = postorder(self.root)
        self.status_label.setText(f"Starting {algo_name} traversal...")

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
            val, visited = next(self.generator)
            self.status_label.setText(f"Visiting Node: {val} | Traversed order: {visited}")
            self.draw_tree(val, visited)
        except StopIteration:
            self.timer.stop()
            self.generator = None
            self.status_label.setText("🎉 Tree traversal complete!")

    def update_complexity_info(self, algo_name=None):
        if not algo_name:
            algo_name = self.algo_selector.currentText()
        complexities = {
            "Inorder": {"time": "O(n)", "space": "O(h)", "desc": "Left → Root → Right (yields sorted sequence in BST)"},
            "Preorder": {"time": "O(n)", "space": "O(h)", "desc": "Root → Left → Right (serialization & cloning)"},
            "Postorder": {"time": "O(n)", "space": "O(h)", "desc": "Left → Right → Root (bottom-up deletion)"},
        }
        info = complexities.get(algo_name, {"time": "N/A", "space": "N/A", "desc": ""})
        p = get_mpl_palette()
        self.complexity_label.setText(
            f"⏱ <b>Time Complexity:</b> <span style='color:{p['primary']}'>{info['time']}</span> &nbsp;|&nbsp; "
            f"💾 <b>Space:</b> <span style='color:{p['success']}'>{info['space']}</span> (height h) &nbsp;|&nbsp; "
            f"📌 <i><span style='color:{p['text']}'>{info['desc']}</span></i>"
        )