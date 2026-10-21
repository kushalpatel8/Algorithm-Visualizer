from algorithms.slidingWindow.longestSubstring import longest_substring_k_distinct
from algorithms.slidingWindow.maxSumSubarray import max_sum_subarray
from ui.controls import ControlPanel
from ui.styles import apply_mpl_theme, get_mpl_palette

import random
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel, QHBoxLayout
from PySide6.QtCore import QTimer, Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class SlidingVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        
        # Algorithm Selector
        layout.addWidget(QLabel("Select Sliding Window Algorithm:"))
        self.algo_selector = QComboBox()
        self.algo_selector.addItems(["Max Sum Subarray (Fixed)", "Longest Substring K Distinct (Variable)"])
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
        self.figure, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # Current Sum/Length Label Bar
        res_layout = QHBoxLayout()
        self.cur_label = QLabel("Current Window Result: -")
        self.cur_label.setStyleSheet("font-weight: 700; font-size: 13px;")
        self.max_label = QLabel("Best So Far: -")
        self.max_label.setStyleSheet("font-weight: 700; font-size: 13px;")
        res_layout.addWidget(self.cur_label)
        res_layout.addWidget(self.max_label)
        layout.addLayout(res_layout)
        
        # Control Panel
        self.controls = ControlPanel()
        layout.addWidget(self.controls)
        
        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_step)
        self.generator = None
        self.speed = 50
        self.last_left = -1
        self.last_right = -1
        
        # Data
        self.arr = []
        self.s = "abacbebebe"
        self.n = 20
        self.reset_data()
        
        # Connections
        self.controls.play_clicked.connect(self.start_animation)
        self.controls.pause_clicked.connect(self.pause_animation)
        self.controls.step_clicked.connect(self.single_step)
        self.controls.reset_clicked.connect(self.reset_data)
        self.controls.speed_changed.connect(self.set_speed)

    def update_theme(self):
        if self.algo_selector.currentIndex() == 0:
            self.draw_array(self.last_left, self.last_right)
        else:
            self.draw_string(self.last_left, self.last_right)

    def reset_data(self):
        self.pause_animation()
        self.arr = [random.randint(1, 20) for _ in range(self.n)]
        self.s = "abacbebebe"
        self.status_label.setText("Window initialized. Ready to slide.")
        self.cur_label.setText("Current Window Result: -")
        self.max_label.setText("Best So Far: -")
        self.last_left = -1
        self.last_right = -1
        if self.algo_selector.currentIndex() == 0:
            self.draw_array(-1, -1)
        else:
            self.draw_string(-1, -1)
        self.generator = None

    def draw_array(self, left, right):
        self.last_left = left
        self.last_right = right
        self.ax.clear()
        apply_mpl_theme(self.figure, self.ax)
        p = get_mpl_palette()
        
        colors = [p['inactive']] * self.n
        if left != -1 and right != -1:
            for i in range(left, right + 1):
                if i < self.n:
                    colors[i] = p['primary']
                    
        self.ax.bar(range(self.n), self.arr, color=colors, edgecolor=p['border'], linewidth=0.6, width=0.85)
        self.ax.set_ylim(0, max(self.arr) + 5 if self.arr else 25)
        self.ax.set_xlim(-0.8, self.n - 0.2)
        self.figure.tight_layout()
        self.canvas.draw()

    def draw_string(self, left, right):
        self.last_left = left
        self.last_right = right
        self.ax.clear()
        apply_mpl_theme(self.figure, self.ax)
        p = get_mpl_palette()
        
        n = len(self.s)
        for i, char in enumerate(self.s):
            in_window = (left <= i <= right)
            color = p['primary'] if in_window else p['inactive']
            self.ax.text(i / n + 0.05, 0.5, char, fontsize=24, color=color, 
                         ha='center', va='center', fontweight='bold', family='monospace')
                         
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.axis('off')
        self.figure.tight_layout()
        self.canvas.draw()

    def init_generator(self):
        if self.algo_selector.currentIndex() == 0:
            self.generator = max_sum_subarray(self.arr, 3)
            self.status_label.setText("Computing Max Sum Subarray of size k=3...")
        else:
            self.generator = longest_substring_k_distinct(self.s, 2)
            self.status_label.setText("Computing Longest Substring with at most k=2 distinct chars...")

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
            left, right = res[0], res[1]
            if self.algo_selector.currentIndex() == 0:
                cur_sum, max_sum = res[2], res[3]
                self.cur_label.setText(f"Current Window Sum: {cur_sum}")
                self.max_label.setText(f"Max Sum Found: {max_sum}")
                self.status_label.setText(f"Window [{left}..{right}] -> Sum = {cur_sum} (Max so far: {max_sum})")
                self.draw_array(left, right)
            else:
                max_len = res[2]
                window_len = right - left + 1
                self.cur_label.setText(f"Current Window Length: {window_len}")
                self.max_label.setText(f"Max Substring Length: {max_len}")
                self.status_label.setText(f"Window [{left}..{right}] ('{self.s[left:right+1]}') -> Length = {window_len}")
                self.draw_string(left, right)
        except StopIteration:
            self.timer.stop()
            self.generator = None
            self.status_label.setText("🎉 Sliding Window search complete!")

    def update_complexity_info(self, algo_name=None):
        if not algo_name:
            algo_name = self.algo_selector.currentText()
        complexities = {
            "Max Sum Subarray (Fixed)": {"time": "O(n)", "space": "O(1)", "type": "Fixed window of size k"},
            "Longest Substring K Distinct (Variable)": {"time": "O(n)", "space": "O(k)", "type": "Variable sliding window with hash map"},
        }
        info = complexities.get(algo_name, {"time": "N/A", "space": "N/A", "type": ""})
        p = get_mpl_palette()
        self.complexity_label.setText(
            f"⏱ <b>Time Complexity:</b> <span style='color:{p['primary']}'>{info['time']}</span> &nbsp;|&nbsp; "
            f"💾 <b>Space Complexity:</b> <span style='color:{p['success']}'>{info['space']}</span> &nbsp;|&nbsp; "
            f"🪟 <i><span style='color:{p['text']}'>{info['type']}</span></i>"
        )