from algorithms.dp.coinChange import coin_change
from algorithms.dp.knapsack import knapsack
from algorithms.dp.lcs import lcs
from algorithms.dp.fibonacci import fibonacci

from ui.styles import apply_mpl_theme, get_mpl_palette, get_current_theme_id
from ui.controls import ControlPanel

import numpy as np
import seaborn as sns
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel
from PySide6.QtCore import QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class DPVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        
        # Algorithm Selector
        layout.addWidget(QLabel("Select DP Algorithm:"))
        self.algo_selector = QComboBox()
        self.algo_selector.addItems(["Fibonacci", "Knapsack", "Longest Common Subsequence", "Coin Change"])
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
        
        # Control Panel
        self.controls = ControlPanel()
        layout.addWidget(self.controls)
        
        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_step)
        self.generator = None
        self.speed = 50
        self.last_dp = None
        self.last_highlighted = None
        
        # Data
        self.reset_data()
        
        # Connections
        self.controls.play_clicked.connect(self.start_animation)
        self.controls.pause_clicked.connect(self.pause_animation)
        self.controls.step_clicked.connect(self.single_step)
        self.controls.reset_clicked.connect(self.reset_data)
        self.controls.speed_changed.connect(self.set_speed)

    def update_theme(self):
        if self.last_dp is not None:
            self.draw_dp(self.last_dp, self.last_highlighted)
        else:
            self.reset_data()

    def reset_data(self):
        self.pause_animation()
        self.ax.clear()
        apply_mpl_theme(self.figure, self.ax)
        self.status_label.setText("Ready to compute DP table.")
        self.canvas.draw()
        self.generator = None
        self.last_dp = None
        self.last_highlighted = None

    def draw_dp(self, dp, highlighted):
        self.last_dp = dp
        self.last_highlighted = highlighted
        self.ax.clear()
        apply_mpl_theme(self.figure, self.ax)
        p = get_mpl_palette()
        tid = get_current_theme_id()
        
        cmap_map = {
            "emerald": "crest",
            "sunset": "YlOrRd",
            "violet": "mako",
            "monokai": "magma",
            "light": "Blues"
        }
        chosen_cmap = cmap_map.get(tid, "mako")
        
        if isinstance(dp[0], list): # 2D DP Table
            data = np.array(dp)
            sns.heatmap(data, annot=True, fmt="d", cmap=chosen_cmap, ax=self.ax, cbar=False,
                        linewidths=1.0, linecolor=p['fig_bg'],
                        annot_kws={"size": 11, "weight": "bold", "color": "white" if tid != "light" else "black"})
            if highlighted:
                i, j = highlighted
                self.ax.add_patch(plt.Rectangle((j, i), 1, 1, fill=False, edgecolor=p['highlight'], lw=3.5))
            algo = self.algo_selector.currentText()
            self.ax.set_title(f"{algo} DP Table", color=p['text'], fontsize=12, fontweight='bold', pad=10)
        else: # 1D DP (Fibonacci)
            bars = self.ax.bar(range(len(dp)), dp, color=p['primary'], edgecolor=p['edge'], linewidth=0.6)
            for idx in highlighted:
                if 0 <= idx < len(dp):
                    bars[idx].set_color(p['highlight'])
            self.ax.set_title("Fibonacci Sequence DP Array", color=p['text'], fontsize=12, fontweight='bold', pad=10)
            
        self.figure.tight_layout()
        self.canvas.draw()

    def init_generator(self):
        algo_name = self.algo_selector.currentText()
        if algo_name == "Fibonacci":
            self.generator = fibonacci(12)
            self.status_label.setText("Building Fibonacci numbers 0..12 bottom-up...")
        elif algo_name == "Knapsack":
            weights = [2, 3, 4, 5]
            values = [3, 4, 5, 6]
            capacity = 5
            self.generator = knapsack(weights, values, capacity)
            self.status_label.setText("Filling 0/1 Knapsack table (Capacity: 5, Items: 4)...")
        elif algo_name == "Longest Common Subsequence":
            self.generator = lcs("ABCBDAB", "BDCABA")
            self.status_label.setText("Filling LCS table for 'ABCBDAB' vs 'BDCABA'...")
        elif algo_name == "Coin Change":
            coins = [1, 2, 5]
            amount = 7
            self.generator = coin_change(coins, amount)
            self.status_label.setText("Filling Coin Change table (Coins: [1, 2, 5], Target: 7)...")

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
            dp, highlighted = next(self.generator)
            self.draw_dp(dp, highlighted)
        except StopIteration:
            self.timer.stop()
            self.generator = None
            self.status_label.setText("🎉 DP Table computation completed!")

    def update_complexity_info(self, algo_name=None):
        if not algo_name:
            algo_name = self.algo_selector.currentText()
        complexities = {
            "Fibonacci": {"time": "O(n)", "space": "O(n)", "desc": "Bottom-up tabulation"},
            "Knapsack": {"time": "O(n · W)", "space": "O(n · W)", "desc": "0/1 Knapsack dynamic programming"},
            "Longest Common Subsequence": {"time": "O(m · n)", "space": "O(m · n)", "desc": "2D LCS character match grid"},
            "Coin Change": {"time": "O(n · amount)", "space": "O(n · amount)", "desc": "Minimum coin combinations"},
        }
        info = complexities.get(algo_name, {"time": "N/A", "space": "N/A", "desc": ""})
        p = get_mpl_palette()
        self.complexity_label.setText(
            f"⏱ <b>Time Complexity:</b> <span style='color:{p['primary']}'>{info['time']}</span> &nbsp;|&nbsp; "
            f"💾 <b>Space Complexity:</b> <span style='color:{p['success']}'>{info['space']}</span> &nbsp;|&nbsp; "
            f"📌 <i><span style='color:{p['text']}'>{info['desc']}</span></i>"
        )