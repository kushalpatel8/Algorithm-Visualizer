from algorithms.searching.binarySearch import binary_search
from algorithms.searching.exponentialSearch import exponential_search
from algorithms.searching.jumpSearch import jump_search
from algorithms.searching.linearSearch import linear_search 
from algorithms.searching.ternarySearch import ternary_search
from ui.controls import ControlPanel
from ui.styles import apply_mpl_theme, get_mpl_palette

import random
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel, QLineEdit, QHBoxLayout
from PySide6.QtCore import QTimer, Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class SearchingVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        
        # Algorithm Selector & Input
        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)
        
        top_layout.addWidget(QLabel("Select Algorithm:"))
        self.algo_selector = QComboBox()
        self.algo_selector.addItems([
            "Linear Search", 
            "Binary Search",
            "Jump Search",
            "Ternary Search",
            "Exponential Search"
        ])
        top_layout.addWidget(self.algo_selector)
        
        top_layout.addWidget(QLabel("Target Value:"))
        self.target_input = QLineEdit("25")
        self.target_input.setFixedWidth(100)
        top_layout.addWidget(self.target_input)
        top_layout.addStretch()
        layout.addLayout(top_layout)
        
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
        self.figure, self.ax = plt.subplots(figsize=(8, 4))
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
        self.n = 50
        self.arr = []
        self.reset_data()
        
        # Connections
        self.controls.play_clicked.connect(self.start_animation)
        self.controls.pause_clicked.connect(self.pause_animation)
        self.controls.step_clicked.connect(self.single_step)
        self.controls.reset_clicked.connect(self.reset_data)
        self.controls.speed_changed.connect(self.set_speed)

    def update_theme(self):
        self.draw_array()

    def reset_data(self):
        self.pause_animation()
        self.arr = sorted(random.sample(range(1, 101), self.n))
        default_target = self.arr[len(self.arr) // 2]
        self.target_input.setText(str(default_target))
        self.status_label.setText(f"Array initialized with {self.n} sorted integers. Target: {default_target}")
        self.draw_array()
        self.generator = None

    def draw_array(self, highlighted=-1, found=False, low=0, high=49):
        self.ax.clear()
        apply_mpl_theme(self.figure, self.ax)
        p = get_mpl_palette()
        
        colors = [p['inactive']] * self.n
        for i in range(self.n):
            if low <= i <= high:
                colors[i] = p['primary']
        
        if highlighted != -1 and 0 <= highlighted < self.n:
            colors[highlighted] = p['success'] if found else p['highlight']
            
        self.ax.bar(range(self.n), self.arr, color=colors, edgecolor=p['border'], linewidth=0.5, width=0.85)
        self.ax.set_ylim(0, 110)
        self.ax.set_xlim(-0.8, self.n - 0.2)
        self.figure.tight_layout()
        self.canvas.draw()

    def init_generator(self):
        try:
            target = int(self.target_input.text())
        except ValueError:
            target = 25
        
        algo_name = self.algo_selector.currentText()
        if algo_name == "Linear Search":
            self.generator = linear_search(self.arr, target)
        elif algo_name == "Binary Search":
            self.generator = binary_search(self.arr, target)
        elif algo_name == "Jump Search":
            self.generator = jump_search(self.arr, target)
        elif algo_name == "Ternary Search":
            self.generator = ternary_search(self.arr, target)
        elif algo_name == "Exponential Search":
            self.generator = exponential_search(self.arr, target)
            
        self.status_label.setText(f"Searching for {target} using {algo_name}...")

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
            if len(res) == 2:
                idx, found = res
                self.draw_array(idx, found)
                if found:
                    self.status_label.setText(f"🎉 Target found at index {idx} (value {self.arr[idx]})!")
            else:
                idx, found, low, high = res
                self.draw_array(idx, found, low, high)
                if found:
                    self.status_label.setText(f"🎉 Target found at index {idx} (value {self.arr[idx]})!")
                elif idx != -1:
                    self.status_label.setText(f"Inspecting index {idx} (value {self.arr[idx]}) | Active window: [{low}..{high}]")
                else:
                    self.status_label.setText("Target not found in array.")
        except StopIteration:
            self.timer.stop()
            self.generator = None

    def update_complexity_info(self, algo_name=None):
        if not algo_name:
            algo_name = self.algo_selector.currentText()
        complexities = {
            "Linear Search": {"best": "O(1)", "worst": "O(n)", "space": "O(1)", "req": "Unsorted or sorted"},
            "Binary Search": {"best": "O(1)", "worst": "O(log n)", "space": "O(1)", "req": "Sorted array only"},
            "Jump Search": {"best": "O(1)", "worst": "O(√n)", "space": "O(1)", "req": "Sorted array only"},
            "Ternary Search": {"best": "O(1)", "worst": "O(log₃ n)", "space": "O(1)", "req": "Sorted array only"},
            "Exponential Search": {"best": "O(1)", "worst": "O(log n)", "space": "O(1)", "req": "Sorted array only"},
        }
        info = complexities.get(algo_name, {"best": "N/A", "worst": "N/A", "space": "N/A", "req": ""})
        p = get_mpl_palette()
        self.complexity_label.setText(
            f"⏱ <b>Best:</b> <span style='color:{p['primary']}'>{info['best']}</span> &nbsp;|&nbsp; "
            f"<b>Worst:</b> <span style='color:{p['highlight']}'>{info['worst']}</span> &nbsp;|&nbsp; "
            f"💾 <b>Space:</b> <span style='color:{p['success']}'>{info['space']}</span> &nbsp;|&nbsp; "
            f"📋 <b>Requirement:</b> <span style='color:{p['text']}'>{info['req']}</span>"
        )