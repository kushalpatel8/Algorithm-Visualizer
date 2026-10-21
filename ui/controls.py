from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QPushButton, QSlider, QLabel, QVBoxLayout, QFrame)

class ControlPanel(QWidget):
    play_clicked = Signal()
    pause_clicked = Signal()
    step_clicked = Signal()
    reset_clicked = Signal()
    speed_changed = Signal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 4, 0, 0)
        
        # Container bar
        container = QFrame()
        container.setObjectName("control_panel_bar")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)
        
        # Control Buttons
        self.play_btn = QPushButton("▶  Play")
        self.play_btn.setObjectName("btn_play")
        self.play_btn.setCursor(Qt.PointingHandCursor)
        self.play_btn.setToolTip("Start algorithm animation")
        
        self.pause_btn = QPushButton("⏸  Pause")
        self.pause_btn.setObjectName("btn_pause")
        self.pause_btn.setCursor(Qt.PointingHandCursor)
        self.pause_btn.setToolTip("Pause animation")
        
        self.step_btn = QPushButton("⏭  Step")
        self.step_btn.setObjectName("btn_step")
        self.step_btn.setCursor(Qt.PointingHandCursor)
        self.step_btn.setToolTip("Advance exactly one step forward")
        
        self.reset_btn = QPushButton("🔄  Reset")
        self.reset_btn.setObjectName("btn_reset")
        self.reset_btn.setCursor(Qt.PointingHandCursor)
        self.reset_btn.setToolTip("Shuffle data and reset state")
        
        # Speed Slider
        speed_container = QWidget()
        speed_layout = QVBoxLayout(speed_container)
        speed_layout.setContentsMargins(10, 0, 10, 0)
        speed_layout.setSpacing(2)
        
        self.speed_label = QLabel("⚡ Speed: 50x")
        self.speed_label.setStyleSheet("font-size: 11px; font-weight: 700; color: #94a3b8;")
        
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(1, 100)
        self.speed_slider.setValue(50)
        self.speed_slider.setCursor(Qt.PointingHandCursor)
        self.speed_slider.valueChanged.connect(self.update_speed_label)
        
        speed_layout.addWidget(self.speed_label)
        speed_layout.addWidget(self.speed_slider)
        
        # Connections
        self.play_btn.clicked.connect(self.play_clicked.emit)
        self.pause_btn.clicked.connect(self.pause_clicked.emit)
        self.step_btn.clicked.connect(self.step_clicked.emit)
        self.reset_btn.clicked.connect(self.reset_clicked.emit)
        self.speed_slider.valueChanged.connect(self.speed_changed.emit)
        
        layout.addWidget(self.play_btn)
        layout.addWidget(self.pause_btn)
        layout.addWidget(self.step_btn)
        layout.addWidget(self.reset_btn)
        layout.addWidget(speed_container, 1)
        
        outer_layout.addWidget(container)

    def update_speed_label(self, value):
        self.speed_label.setText(f"⚡ Speed: {value}x")
        