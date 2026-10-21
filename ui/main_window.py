import sys
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QStackedWidget, QLabel, QFrame, QComboBox)
from PySide6.QtCore import Qt

from ui.styles import THEMES, set_current_theme, get_theme_qss, get_current_theme_id
from visualizer.dp_visualizer import DPVisualizer
from visualizer.graph_visualizer import GraphVisualizer
from visualizer.searching_visualizer import SearchingVisualizer
from visualizer.sliding_visualizer import SlidingVisualizer
from visualizer.sorting_visualizer import SortingVisualizer
from visualizer.string_visualizer import StringVisualizer
from visualizer.tree_visualizer import TreeVisualizer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Algorithm Visualizer Studio")
        self.resize(1300, 850)
        self.setMinimumSize(1000, 700)
        
        # Initial Theme: Emerald Studio (Non-blue!)
        set_current_theme("emerald")
        self.setStyleSheet(get_theme_qss("emerald"))
        
        # Main layout
        central_widget = QWidget()
        central_widget.setObjectName("central_widget")
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- Sidebar Container ---
        sidebar_container = QWidget()
        sidebar_container.setObjectName("sidebar_container")
        sidebar_container.setFixedWidth(240)
        sidebar_layout = QVBoxLayout(sidebar_container)
        sidebar_layout.setContentsMargins(14, 18, 14, 16)
        sidebar_layout.setSpacing(10)
        
        # Brand Header
        brand_widget = QWidget()
        brand_layout = QVBoxLayout(brand_widget)
        brand_layout.setContentsMargins(4, 0, 4, 6)
        brand_layout.setSpacing(2)
        
        title_label = QLabel("🧠 ALGO STUDIO")
        title_label.setObjectName("brand_title")
        subtitle_label = QLabel("Interactive DSA Visualizer")
        subtitle_label.setObjectName("brand_subtitle")
        
        brand_layout.addWidget(title_label)
        brand_layout.addWidget(subtitle_label)
        sidebar_layout.addWidget(brand_widget)
        
        # Theme Selector Box
        theme_box = QWidget()
        theme_box_layout = QVBoxLayout(theme_box)
        theme_box_layout.setContentsMargins(0, 0, 0, 6)
        theme_box_layout.setSpacing(4)
        
        theme_lbl = QLabel("🎨 THEME")
        theme_lbl.setStyleSheet("font-size: 10px; font-weight: 800; letter-spacing: 1px; padding-left: 2px;")
        
        self.theme_selector = QComboBox()
        self.theme_keys = ["emerald", "sunset", "violet", "monokai", "light"]
        for k in self.theme_keys:
            self.theme_selector.addItem(THEMES[k]["name"], k)
            
        self.theme_selector.setCurrentIndex(0)
        self.theme_selector.currentIndexChanged.connect(self.on_theme_changed)
        
        theme_box_layout.addWidget(theme_lbl)
        theme_box_layout.addWidget(self.theme_selector)
        sidebar_layout.addWidget(theme_box)
        
        # Category Section Label
        section_lbl = QLabel("CATEGORIES")
        section_lbl.setStyleSheet("font-size: 10px; font-weight: 800; letter-spacing: 1px; padding-left: 2px;")
        sidebar_layout.addWidget(section_lbl)
        
        # Sidebar List with clean icons
        self.sidebar = QListWidget()
        categories = [
            "🔢   Sorting",
            "🔍   Searching",
            "🕸️   Graphs",
            "🌳   Trees",
            "🪟   Sliding Window",
            "📐   Dynamic Prog.",
            "🔤   String Search"
        ]
        self.sidebar.addItems(categories)
        self.sidebar.currentRowChanged.connect(self.switch_visualizer)
        sidebar_layout.addWidget(self.sidebar, 1)
        
        # Sidebar Footer Info Box
        footer_box = QFrame()
        footer_box.setStyleSheet(
            "border-radius: 8px; padding: 10px; border: 1px solid rgba(255, 255, 255, 0.08);"
        )
        footer_layout = QVBoxLayout(footer_box)
        footer_layout.setContentsMargins(4, 4, 4, 4)
        footer_layout.setSpacing(4)
        
        footer_badge = QLabel("⚡ 38+ Algorithms")
        footer_badge.setStyleSheet("font-weight: 700; font-size: 11px;")
        footer_tip = QLabel("Click 🎨 Theme above to switch palettes.")
        footer_tip.setWordWrap(True)
        footer_tip.setStyleSheet("font-size: 11px;")
        
        footer_layout.addWidget(footer_badge)
        footer_layout.addWidget(footer_tip)
        sidebar_layout.addWidget(footer_box)
        
        # --- Content Area Stack ---
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(16, 16, 16, 16)
        
        self.stack = QStackedWidget()
        self.stack.setObjectName("visualizer_card")
        
        # Visualizers instantiation
        self.sorting_visualizer = SortingVisualizer()
        self.searching_visualizer = SearchingVisualizer()
        self.graph_visualizer = GraphVisualizer()
        self.tree_visualizer = TreeVisualizer()
        self.sliding_visualizer = SlidingVisualizer()
        self.dp_visualizer = DPVisualizer()
        self.string_visualizer = StringVisualizer()
        
        self.stack.addWidget(self.sorting_visualizer)
        self.stack.addWidget(self.searching_visualizer)
        self.stack.addWidget(self.graph_visualizer)
        self.stack.addWidget(self.tree_visualizer)
        self.stack.addWidget(self.sliding_visualizer)
        self.stack.addWidget(self.dp_visualizer)
        self.stack.addWidget(self.string_visualizer)
        
        content_layout.addWidget(self.stack)
        
        # Add to main layout
        main_layout.addWidget(sidebar_container)
        main_layout.addWidget(content_container, 1)
        
        # Initial selection
        self.sidebar.setCurrentRow(0)

    def switch_visualizer(self, index):
        self.stack.setCurrentIndex(index)

    def on_theme_changed(self, index):
        theme_id = self.theme_selector.currentData()
        if not theme_id:
            theme_id = self.theme_keys[index]
            
        set_current_theme(theme_id)
        self.setStyleSheet(get_theme_qss(theme_id))
        
        # Update all visualizers and re-render charts
        self.sorting_visualizer.update_theme()
        self.searching_visualizer.update_theme()
        self.graph_visualizer.update_theme()
        self.tree_visualizer.update_theme()
        self.sliding_visualizer.update_theme()
        self.dp_visualizer.update_theme()
        self.string_visualizer.update_theme()
        
        # Update complexity labels
        self.sorting_visualizer.update_complexity_info()
        self.searching_visualizer.update_complexity_info()
        self.graph_visualizer.update_complexity_info()
        self.tree_visualizer.update_complexity_info()
        self.sliding_visualizer.update_complexity_info()
        self.dp_visualizer.update_complexity_info()
        self.string_visualizer.update_complexity_info()

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())