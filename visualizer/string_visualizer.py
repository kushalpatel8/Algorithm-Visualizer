from algorithms.string.kmp import kmp_search
from algorithms.string.byoreMoore import boyer_moore 
from algorithms.string.robinKarp import rabin_karp
from ui.controls import ControlPanel
from ui.styles import apply_mpl_theme, get_mpl_palette

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QComboBox, QLabel, QLineEdit, QHBoxLayout, QPushButton)
from PySide6.QtCore import QTimer, Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.patches as patches

class StringVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        
        # Algorithm Selector & Input Fields
        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)
        
        self.algo_selector = QComboBox()
        self.algo_selector.addItems(["KMP Search", "Rabin-Karp", "Boyer-Moore"])
        top_layout.addWidget(QLabel("Algorithm:"))
        top_layout.addWidget(self.algo_selector)
        
        self.text_input = QLineEdit("ABCBDABACDABABCBD")
        top_layout.addWidget(QLabel("Text:"))
        top_layout.addWidget(self.text_input)
        
        self.pattern_input = QLineEdit("ABC")
        self.pattern_input.setFixedWidth(90)
        top_layout.addWidget(QLabel("Pattern:"))
        top_layout.addWidget(self.pattern_input)
        
        # Preset buttons
        btn_preset1 = QPushButton("Example 1")
        btn_preset1.setToolTip("Text: ABCBDABACDABABCBD | Pattern: ABC")
        btn_preset1.clicked.connect(lambda: self.load_preset("ABCBDABACDABABCBD", "ABC"))
        top_layout.addWidget(btn_preset1)
        
        btn_preset2 = QPushButton("DNA Match")
        btn_preset2.setToolTip("Text: ATCGATCGAATCG | Pattern: ATCG")
        btn_preset2.clicked.connect(lambda: self.load_preset("ATCGATCGAATCG", "ATCG"))
        top_layout.addWidget(btn_preset2)
        
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
        
        # Matplotlib Figure with dynamic theme
        self.figure, self.ax = plt.subplots(figsize=(10, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        self.update_complexity_info()
        
        # Control Panel
        self.controls = ControlPanel()
        layout.addWidget(self.controls)
        
        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_step)
        self.generator = None
        self.speed = 50
        
        # State tracking
        self.found_indices = set()
        self.current_shift = 0
        self.current_text_idx = -1
        self.current_pattern_idx = -1
        self.current_status = "idle"
        self.extra_info = {}
        
        # Connect text/pattern edits to reset
        self.text_input.textChanged.connect(self.reset_data)
        self.pattern_input.textChanged.connect(self.reset_data)
        
        # Connections
        self.controls.play_clicked.connect(self.start_animation)
        self.controls.pause_clicked.connect(self.pause_animation)
        self.controls.step_clicked.connect(self.single_step)
        self.controls.reset_clicked.connect(self.reset_data)
        self.controls.speed_changed.connect(self.set_speed)
        
        self.reset_data()

    def update_theme(self):
        self.draw_tiles()

    def load_preset(self, text, pattern):
        self.text_input.setText(text)
        self.pattern_input.setText(pattern)
        self.reset_data()

    def reset_data(self):
        self.pause_animation()
        self.found_indices = set()
        self.current_shift = 0
        self.current_text_idx = -1
        self.current_pattern_idx = -1
        self.current_status = "idle"
        self.extra_info = {}
        self.status_label.setText("Ready to start search. Click ▶ Play or ⏭ Step.")
        self.draw_tiles()
        self.generator = None

    def draw_tiles(self):
        self.ax.clear()
        apply_mpl_theme(self.figure, self.ax)
        p = get_mpl_palette()
        
        text = self.text_input.text()
        pattern = self.pattern_input.text()
        n = len(text)
        m = len(pattern)
        
        if n == 0 or m == 0:
            self.ax.text(0.5, 0.5, "Please enter non-empty Text and Pattern.", 
                         ha='center', va='center', fontsize=14, color=p['text'], transform=self.ax.transAxes)
            self.ax.axis('off')
            self.canvas.draw()
            return
            
        box_width = 0.8
        box_height = 0.22
        
        # 1. Draw Text Row at y = 0.55
        y_text = 0.55
        self.ax.text(-0.7, y_text + box_height / 2, "Text:", va='center', ha='right', 
                     fontsize=11, fontweight='bold', color=p['text'])
                     
        for i, char in enumerate(text):
            x = i
            is_found = any(fi <= i < fi + m for fi in self.found_indices)
            if is_found:
                facecolor = p['border']
                textcolor = p['success']
                edgecolor = p['success']
            elif i == self.current_text_idx:
                if self.current_status in ["match", "found"]:
                    facecolor = p['border']
                    textcolor = p['success']
                    edgecolor = p['success']
                elif self.current_status == "mismatch":
                    facecolor = p['border']
                    textcolor = p['highlight']
                    edgecolor = p['highlight']
                else:
                    facecolor = p['border']
                    textcolor = p['primary']
                    edgecolor = p['primary']
            elif self.current_shift <= i < self.current_shift + m:
                facecolor = p['ax_bg']
                textcolor = p['primary']
                edgecolor = p['primary']
            else:
                facecolor = p['ax_bg']
                textcolor = p['text']
                edgecolor = p['border']
                
            rect = patches.FancyBboxPatch(
                (x - box_width / 2, y_text), box_width, box_height,
                boxstyle="round,pad=0.04,rounding_size=0.1",
                facecolor=facecolor, edgecolor=edgecolor, linewidth=1.5
            )
            self.ax.add_patch(rect)
            
            # Text character
            self.ax.text(x, y_text + box_height / 2, char, 
                         ha='center', va='center', fontsize=12, fontweight='bold', 
                         color=textcolor, family='monospace')
                         
            # Index label above
            self.ax.text(x, y_text + box_height + 0.04, str(i), 
                         ha='center', va='bottom', fontsize=8, color=p['text'])

        # 2. Draw Pattern Row at y = 0.22
        y_pattern = 0.22
        self.ax.text(-0.7, y_pattern + box_height / 2, "Pattern:", va='center', ha='right', 
                     fontsize=11, fontweight='bold', color=p['text'])
                     
        shift = self.current_shift
        for j, char in enumerate(pattern):
            x = shift + j
            if j == self.current_pattern_idx:
                if self.current_status in ["match", "found"]:
                    facecolor = p['border']
                    textcolor = p['success']
                    edgecolor = p['success']
                elif self.current_status == "mismatch":
                    facecolor = p['border']
                    textcolor = p['highlight']
                    edgecolor = p['highlight']
                else:
                    facecolor = p['border']
                    textcolor = p['primary']
                    edgecolor = p['primary']
            elif self.current_status == "found" and shift in self.found_indices:
                facecolor = p['border']
                textcolor = p['success']
                edgecolor = p['success']
            else:
                facecolor = p['ax_bg']
                textcolor = p['primary']
                edgecolor = p['border']
                
            rect = patches.FancyBboxPatch(
                (x - box_width / 2, y_pattern), box_width, box_height,
                boxstyle="round,pad=0.04,rounding_size=0.1",
                facecolor=facecolor, edgecolor=edgecolor, linewidth=1.5
            )
            self.ax.add_patch(rect)
            
            # Pattern character
            self.ax.text(x, y_pattern + box_height / 2, char, 
                         ha='center', va='center', fontsize=12, fontweight='bold', 
                         color=textcolor, family='monospace')
                         
            # Pattern index below
            self.ax.text(x, y_pattern - 0.04, f"[{j}]", 
                         ha='center', va='top', fontsize=8, color=p['text'])

        # 3. Connection indicator arrow
        if self.current_pattern_idx != -1 and self.current_text_idx != -1:
            arrow_color = p['success'] if self.current_status in ["match", "found"] else p['highlight'] if self.current_status == "mismatch" else p['primary']
            x_pos = self.current_text_idx
            self.ax.annotate(
                "", xy=(x_pos, y_text), xytext=(x_pos, y_pattern + box_height),
                arrowprops=dict(arrowstyle="<->", color=arrow_color, lw=2.2)
            )

        # 4. Extra Algorithm Data Info Line at bottom
        extra_str = ""
        algo_name = self.algo_selector.currentText()
        if algo_name == "KMP Search" and "lps" in self.extra_info:
            extra_str = f"LPS Array: {self.extra_info['lps']}"
        elif algo_name == "Rabin-Karp" and "text_hash" in self.extra_info:
            extra_str = f"Window Hash: {self.extra_info['text_hash']}  |  Pattern Hash: {self.extra_info['pattern_hash']}"
        elif algo_name == "Boyer-Moore" and "bad_char" in self.extra_info:
            bc_str = ", ".join(f"'{k}':{v}" for k, v in sorted(self.extra_info['bad_char'].items()))
            extra_str = f"Bad Character Table: {{{bc_str}}}"
            
        if extra_str:
            self.ax.text(n / 2, 0.03, extra_str, ha='center', va='center', 
                         fontsize=10, color=p['text'], family='monospace',
                         bbox=dict(boxstyle="round,pad=0.4", facecolor=p['ax_bg'], edgecolor=p['border']))

        self.ax.set_xlim(-1.2, max(n, 12) + 0.2)
        self.ax.set_ylim(-0.05, 0.95)
        self.ax.axis('off')
        self.figure.tight_layout()
        self.canvas.draw()

    def init_generator(self):
        text = self.text_input.text()
        pattern = self.pattern_input.text()
        if not text or not pattern:
            self.status_label.setText("Error: Text and Pattern must not be empty.")
            return
            
        algo_name = self.algo_selector.currentText()
        if algo_name == "KMP Search":
            self.generator = kmp_search(text, pattern)
        elif algo_name == "Rabin-Karp":
            self.generator = rabin_karp(text, pattern)
        elif algo_name == "Boyer-Moore":
            self.generator = boyer_moore(text, pattern)
            
        self.status_label.setText(f"Starting {algo_name}...")

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
            self.current_shift = res[0]
            self.current_text_idx = res[1]
            self.current_pattern_idx = res[2]
            self.current_status = res[3] if len(res) > 3 else "match"
            message = res[4] if len(res) > 4 else ""
            self.extra_info = res[5] if len(res) > 5 and isinstance(res[5], dict) else {}
            
            if self.current_status == "found":
                self.found_indices.add(self.current_shift)
                
            prefix = "🎉 " if self.current_status == "found" else "🟢 " if self.current_status == "match" else "🔴 " if self.current_status == "mismatch" else "ℹ️ "
            found_summary = f" (Total matches so far: {len(self.found_indices)})" if self.found_indices else ""
            self.status_label.setText(f"{prefix}{message}{found_summary}")
            self.draw_tiles()
        except StopIteration:
            self.timer.stop()
            self.generator = None
            if self.found_indices:
                sorted_hits = sorted(list(self.found_indices))
                self.status_label.setText(f"🎉 Search complete! Found {len(self.found_indices)} match(es) at indices: {sorted_hits}")
            else:
                self.status_label.setText("Search complete! Pattern was not found in text.")
            self.draw_tiles()

    def update_complexity_info(self, algo_name=None):
        if not algo_name:
            algo_name = self.algo_selector.currentText()
        complexities = {
            "KMP Search": {"best": "O(n + m)", "worst": "O(n + m)", "space": "O(m)", "note": "Prefix function / LPS array skip"},
            "Rabin-Karp": {"best": "O(n + m)", "worst": "O(n · m)", "space": "O(1)", "note": "Rolling polynomial hash matching"},
            "Boyer-Moore": {"best": "O(n / m)", "worst": "O(n · m)", "space": "O(k)", "note": "Bad-character shift heuristic (right-to-left)"},
        }
        info = complexities.get(algo_name, {"best": "N/A", "worst": "N/A", "space": "N/A", "note": ""})
        p = get_mpl_palette()
        self.complexity_label.setText(
            f"⏱ <b>Best:</b> <span style='color:{p['primary']}'>{info['best']}</span> &nbsp;|&nbsp; "
            f"<b>Worst:</b> <span style='color:{p['highlight']}'>{info['worst']}</span> &nbsp;|&nbsp; "
            f"💾 <b>Space:</b> <span style='color:{p['success']}'>{info['space']}</span> &nbsp;|&nbsp; "
            f"📌 <i><span style='color:{p['text']}'>{info['note']}</span></i>"
        )