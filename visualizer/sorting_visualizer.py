from algorithms.sorting.bubbleSorting import bubble_sort
from algorithms.sorting.insertionSort import insertion_sort
from algorithms.sorting.selectionSort import selection_sort
from algorithms.sorting.mergeSort import merge_sort
from algorithms.sorting.quikSort import quick_sort
from algorithms.sorting.radixSort import radix_sort
from algorithms.sorting.countingSort import counting_sort
from algorithms.sorting.cocktailSort import cocktail_shaker_sort
from algorithms.sorting.combSort import comb_sort
from algorithms.sorting.shellSort import shell_sort
from algorithms.sorting.heapSort import heap_sort
from algorithms.sorting.timSort import tim_sort
from algorithms.sorting.gnomeSort import gnome_sort
from ui.controls import ControlPanel
from ui.styles import apply_mpl_theme, get_mpl_palette

import random
import time
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel
from PySide6.QtCore import QTimer, Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class SortingVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        
        # Algorithm Selector
        layout.addWidget(QLabel("Select Sorting Algorithm:"))
        self.algo_selector = QComboBox()
        self.algo_selector.addItems([
            "Bubble Sort",
            "Selection Sort",
            "Insertion Sort",
            "Quick Sort",
            "Merge Sort",
            "Heap Sort",
            "Shell Sort",
            "Cocktail Shaker Sort",
            "Comb Sort",
            "Tim Sort",
            "Gnome Sort",
            "Radix Sort",
            "Counting Sort"
        ])
        layout.addWidget(self.algo_selector)
        
        # Complexity Info Badge
        self.complexity_label = QLabel()
        self.complexity_label.setObjectName("complexity_badge")
        layout.addWidget(self.complexity_label)
        self.algo_selector.currentTextChanged.connect(self.update_complexity_info)
        
        # Matplotlib Figure with dynamic theme
        self.figure, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        self.update_complexity_info()
        
        # Control Panel
        self.controls = ControlPanel()
        layout.addWidget(self.controls)
        
        # Timer for animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_step)
        self.generator = None
        self.speed = 50
        
        # Data
        self.arr = []
        self.n = 50
        self.reset_data()
        
        # Connections
        self.controls.play_clicked.connect(self.start_animation)
        self.controls.pause_clicked.connect(self.pause_animation)
        self.controls.step_clicked.connect(self.single_step)
        self.controls.reset_clicked.connect(self.reset_data)
        self.controls.speed_changed.connect(self.set_speed)

    def update_theme(self):
        self.draw_bars()

    def reset_data(self):
        self.pause_animation()
        self.arr = list(range(1, self.n + 1))
        random.shuffle(self.arr)
        self.draw_bars()
        self.generator = None

    def draw_bars(self, highlighted=[]):
        self.ax.clear()
        apply_mpl_theme(self.figure, self.ax)
        p = get_mpl_palette()
        
        colors = [p['primary']] * self.n
        for idx in highlighted:
            if 0 <= idx < self.n:
                colors[idx] = p['highlight']
                
        self.ax.bar(range(self.n), self.arr, color=colors, edgecolor=p['edge'], linewidth=0.6, width=0.85)
        self.ax.set_ylim(0, self.n + 5)
        self.ax.set_xlim(-0.8, self.n - 0.2)
        self.figure.tight_layout()
        self.canvas.draw()

    def init_generator(self):
        algo_name = self.algo_selector.currentText()
        arr_copy = list(self.arr)
        if algo_name == "Bubble Sort":
            self.generator = bubble_sort(arr_copy)
        elif algo_name == "Selection Sort":
            self.generator = selection_sort(arr_copy)
        elif algo_name == "Insertion Sort":
            self.generator = insertion_sort(arr_copy)
        elif algo_name == "Quick Sort":
            self.generator = quick_sort(arr_copy, 0, len(arr_copy) - 1)
        elif algo_name == "Merge Sort":
            self.generator = merge_sort(arr_copy, 0, len(arr_copy) - 1)
        elif algo_name == "Heap Sort":
            self.generator = heap_sort(arr_copy)
        elif algo_name == "Shell Sort":
            self.generator = shell_sort(arr_copy)
        elif algo_name == "Cocktail Shaker Sort":
            self.generator = cocktail_shaker_sort(arr_copy)
        elif algo_name == "Comb Sort":
            self.generator = comb_sort(arr_copy)
        elif algo_name == "Tim Sort":
            self.generator = tim_sort(arr_copy)
        elif algo_name == "Gnome Sort":
            self.generator = gnome_sort(arr_copy)
        elif algo_name == "Radix Sort":
            self.generator = radix_sort(arr_copy)
        elif algo_name == "Counting Sort":
            self.generator = counting_sort(arr_copy)

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
            self.arr, highlighted = next(self.generator)
            self.draw_bars(highlighted)
        except StopIteration:
            self.timer.stop()
            self.ax.clear()
            apply_mpl_theme(self.figure, self.ax)
            p = get_mpl_palette()
            self.ax.bar(range(self.n), self.arr, color=p['success'], edgecolor=p['edge'], linewidth=0.6, width=0.85)
            self.ax.set_ylim(0, self.n + 5)
            self.ax.set_xlim(-0.8, self.n - 0.2)
            self.figure.tight_layout()
            self.canvas.draw()
            self.generator = None

    def update_complexity_info(self, algo_name=None):
        if not algo_name:
            algo_name = self.algo_selector.currentText()
        complexities = {
            "Bubble Sort": {"best": "O(n)", "avg": "O(n²)", "worst": "O(n²)", "space": "O(1)"},
            "Selection Sort": {"best": "O(n²)", "avg": "O(n²)", "worst": "O(n²)", "space": "O(1)"},
            "Insertion Sort": {"best": "O(n)", "avg": "O(n²)", "worst": "O(n²)", "space": "O(1)"},
            "Quick Sort": {"best": "O(n log n)", "avg": "O(n log n)", "worst": "O(n²)", "space": "O(log n)"},
            "Merge Sort": {"best": "O(n log n)", "avg": "O(n log n)", "worst": "O(n log n)", "space": "O(n)"},
            "Heap Sort": {"best": "O(n log n)", "avg": "O(n log n)", "worst": "O(n log n)", "space": "O(1)"},
            "Shell Sort": {"best": "O(n log n)", "avg": "O(n log² n)", "worst": "O(n²)", "space": "O(1)"},
            "Cocktail Shaker Sort": {"best": "O(n)", "avg": "O(n²)", "worst": "O(n²)", "space": "O(1)"},
            "Comb Sort": {"best": "O(n log n)", "avg": "O(n² / 2^p)", "worst": "O(n²)", "space": "O(1)"},
            "Tim Sort": {"best": "O(n)", "avg": "O(n log n)", "worst": "O(n log n)", "space": "O(n)"},
            "Gnome Sort": {"best": "O(n)", "avg": "O(n²)", "worst": "O(n²)", "space": "O(1)"},
            "Radix Sort": {"best": "O(nk)", "avg": "O(nk)", "worst": "O(nk)", "space": "O(n + k)"},
            "Counting Sort": {"best": "O(n + k)", "avg": "O(n + k)", "worst": "O(n + k)", "space": "O(k)"},
        }
        info = complexities.get(algo_name, {"best": "N/A", "avg": "N/A", "worst": "N/A", "space": "N/A"})
        p = get_mpl_palette()
        self.complexity_label.setText(
            f"⏱ <b>Best:</b> <span style='color:{p['primary']}'>{info['best']}</span> &nbsp;|&nbsp; "
            f"<b>Average:</b> <span style='color:{p['primary']}'>{info['avg']}</span> &nbsp;|&nbsp; "
            f"<b>Worst:</b> <span style='color:{p['highlight']}'>{info['worst']}</span> &nbsp;|&nbsp; "
            f"💾 <b>Space:</b> <span style='color:{p['success']}'>{info['space']}</span>"
        )