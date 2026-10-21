# Dynamic Multi-Theme Engine for Algorithm Visualizer
# Non-blue themes: Emerald Studio, Sunset Amber, Cyberpunk Violet, Monokai Pro, Nordic Light

def generate_qss(cfg):
    return f"""
QMainWindow, QWidget {{
    background-color: {cfg['bg_main']};
    color: {cfg['text_main']};
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', Roboto, sans-serif;
    font-size: 13px;
}}

#central_widget {{
    background-color: {cfg['bg_main']};
}}

#sidebar_container {{
    background-color: {cfg['bg_sidebar']};
    border-right: 1px solid {cfg['border']};
}}

#brand_title {{
    color: {cfg['text_main']};
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 0.5px;
}}

#brand_subtitle {{
    color: {cfg['text_muted']};
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.3px;
}}

QListWidget {{
    background-color: transparent;
    border: none;
    outline: none;
    padding: 6px;
}}

QListWidget::item {{
    color: {cfg['text_muted']};
    background-color: transparent;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 4px;
    font-size: 13px;
    font-weight: 600;
}}

QListWidget::item:hover {{
    background-color: {cfg['bg_card']};
    color: {cfg['text_main']};
}}

QListWidget::item:selected {{
    background: {cfg['accent_gradient']};
    color: #ffffff;
    font-weight: 700;
}}

#visualizer_card {{
    background-color: {cfg['bg_card']};
    border: 1px solid {cfg['border']};
    border-radius: 12px;
}}

QLabel {{
    color: {cfg['text_muted']};
    font-size: 13px;
}}

#header_label {{
    color: {cfg['text_main']};
    font-size: 15px;
    font-weight: 700;
}}

#complexity_badge {{
    background-color: {cfg['bg_card']};
    border: 1px solid {cfg['border']};
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 13px;
    color: {cfg['text_main']};
}}

#status_banner {{
    background-color: {cfg['bg_sidebar']};
    border: 1px solid {cfg['border']};
    border-radius: 8px;
    padding: 8px 14px;
    font-weight: 600;
    color: {cfg['text_main']};
    font-size: 13px;
}}

QLineEdit {{
    background-color: {cfg['bg_card']};
    border: 1px solid {cfg['border']};
    border-radius: 7px;
    padding: 7px 12px;
    color: {cfg['text_main']};
    font-size: 13px;
    font-weight: 500;
    selection-background-color: {cfg['accent']};
}}

QLineEdit:focus {{
    border: 1px solid {cfg['accent']};
}}

QComboBox {{
    background-color: {cfg['bg_card']};
    border: 1px solid {cfg['border']};
    border-radius: 7px;
    padding: 7px 12px;
    color: {cfg['text_main']};
    font-size: 13px;
    font-weight: 600;
    min-width: 170px;
}}

QComboBox:hover {{
    border: 1px solid {cfg['accent']};
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 26px;
    border-left: 1px solid {cfg['border']};
    border-top-right-radius: 7px;
    border-bottom-right-radius: 7px;
}}

QComboBox QAbstractItemView {{
    background-color: {cfg['bg_card']};
    border: 1px solid {cfg['border']};
    border-radius: 8px;
    padding: 4px;
    color: {cfg['text_main']};
    selection-background-color: {cfg['accent']};
    selection-color: #ffffff;
    outline: none;
}}

QComboBox QAbstractItemView::item {{
    padding: 8px 12px;
    border-radius: 5px;
}}

QPushButton {{
    background-color: {cfg['bg_card']};
    border: 1px solid {cfg['border']};
    border-radius: 7px;
    padding: 7px 14px;
    color: {cfg['text_main']};
    font-weight: 600;
    font-size: 13px;
}}

QPushButton:hover {{
    border-color: {cfg['accent']};
    color: {cfg['text_main']};
}}

#btn_play {{
    background: {cfg['btn_play_gradient']};
    border: 1px solid {cfg['btn_play_border']};
    color: #ffffff;
    font-weight: 700;
    padding: 9px 20px;
    border-radius: 8px;
}}
#btn_play:hover {{
    filter: brightness(1.15);
}}

#btn_pause {{
    background: {cfg['btn_pause_gradient']};
    border: 1px solid {cfg['btn_pause_border']};
    color: #ffffff;
    font-weight: 700;
    padding: 9px 20px;
    border-radius: 8px;
}}

#btn_step {{
    background: {cfg['btn_step_gradient']};
    border: 1px solid {cfg['btn_step_border']};
    color: #ffffff;
    font-weight: 700;
    padding: 9px 18px;
    border-radius: 8px;
}}

#btn_reset {{
    background-color: {cfg['bg_card']};
    border: 1px solid {cfg['border']};
    color: {cfg['text_main']};
    font-weight: 700;
    padding: 9px 18px;
    border-radius: 8px;
}}
#btn_reset:hover {{
    border-color: {cfg['accent']};
}}

#control_panel_bar {{
    background-color: {cfg['bg_card']};
    border: 1px solid {cfg['border']};
    border-radius: 10px;
    padding: 8px 16px;
}}

QSlider::groove:horizontal {{
    height: 6px;
    background: {cfg['border']};
    border-radius: 3px;
}}

QSlider::sub-page:horizontal {{
    background: {cfg['accent_gradient']};
    border-radius: 3px;
}}

QSlider::handle:horizontal {{
    background: #ffffff;
    border: 2px solid {cfg['accent']};
    width: 16px;
    margin-top: -6px;
    margin-bottom: -6px;
    border-radius: 8px;
}}

QScrollBar:vertical {{
    border: none;
    background: {cfg['bg_main']};
    width: 8px;
    margin: 0px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: {cfg['border']};
    min-height: 20px;
    border-radius: 4px;
}}
"""

THEMES = {
    "emerald": {
        "id": "emerald",
        "name": "🌿  Emerald Studio",
        "bg_main": "#0f1512",
        "bg_card": "#15201a",
        "bg_sidebar": "#090d0b",
        "border": "#22332a",
        "text_main": "#f0fdf4",
        "text_muted": "#86a596",
        "accent": "#10b981",
        "accent_hover": "#059669",
        "accent_gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:1 #059669)",
        "btn_play_gradient": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #10b981, stop:1 #059669)",
        "btn_play_border": "#047857",
        "btn_pause_gradient": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f59e0b, stop:1 #d97706)",
        "btn_pause_border": "#b45309",
        "btn_step_gradient": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0d9488, stop:1 #0f766e)",
        "btn_step_border": "#115e59",
        "mpl": {
            "fig_bg": "#0f1512",
            "ax_bg": "#15201a",
            "primary": "#10b981",
            "highlight": "#f43f5e",
            "success": "#34d399",
            "inactive": "#22332a",
            "edge": "#059669",
            "text": "#f0fdf4",
            "border": "#22332a"
        }
    },
    "sunset": {
        "id": "sunset",
        "name": "🌆  Sunset Amber",
        "bg_main": "#171412",
        "bg_card": "#211c19",
        "bg_sidebar": "#0d0b0a",
        "border": "#3b302a",
        "text_main": "#fffbeb",
        "text_muted": "#a89b91",
        "accent": "#f59e0b",
        "accent_hover": "#d97706",
        "accent_gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f59e0b, stop:1 #ea580c)",
        "btn_play_gradient": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f59e0b, stop:1 #ea580c)",
        "btn_play_border": "#c2410c",
        "btn_pause_gradient": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ef4444, stop:1 #dc2626)",
        "btn_pause_border": "#b91c1c",
        "btn_step_gradient": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d97706, stop:1 #b45309)",
        "btn_step_border": "#92400e",
        "mpl": {
            "fig_bg": "#171412",
            "ax_bg": "#211c19",
            "primary": "#f59e0b",
            "highlight": "#ef4444",
            "success": "#10b981",
            "inactive": "#3b302a",
            "edge": "#d97706",
            "text": "#fffbeb",
            "border": "#3b302a"
        }
    },
    "violet": {
        "id": "violet",
        "name": "🔮  Cyberpunk Violet",
        "bg_main": "#120f1c",
        "bg_card": "#1c172b",
        "bg_sidebar": "#0b0813",
        "border": "#2e2447",
        "text_main": "#faf5ff",
        "text_muted": "#9e8eb8",
        "accent": "#a855f7",
        "accent_hover": "#9333ea",
        "accent_gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #a855f7, stop:1 #c026d3)",
        "btn_play_gradient": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a855f7, stop:1 #9333ea)",
        "btn_play_border": "#7e22ce",
        "btn_pause_gradient": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ec4899, stop:1 #db2777)",
        "btn_pause_border": "#be185d",
        "btn_step_gradient": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7c3aed, stop:1 #6d28d9)",
        "btn_step_border": "#5b21b6",
        "mpl": {
            "fig_bg": "#120f1c",
            "ax_bg": "#1c172b",
            "primary": "#a855f7",
            "highlight": "#ec4899",
            "success": "#10b981",
            "inactive": "#2e2447",
            "edge": "#9333ea",
            "text": "#faf5ff",
            "border": "#2e2447"
        }
    },
    "monokai": {
        "id": "monokai",
        "name": "⚡  Monokai Pro",
        "bg_main": "#1c1b1d",
        "bg_card": "#262529",
        "bg_sidebar": "#131214",
        "border": "#3d3b42",
        "text_main": "#fcfcfa",
        "text_muted": "#939293",
        "accent": "#ffd866",
        "accent_hover": "#e6c35c",
        "accent_gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ffd866, stop:1 #fc9867)",
        "btn_play_gradient": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a9dc76, stop:1 #8fbf5c)",
        "btn_play_border": "#78a649",
        "btn_pause_gradient": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ff6188, stop:1 #e04b71)",
        "btn_pause_border": "#c9345a",
        "btn_step_gradient": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #78dce8, stop:1 #5bc2ce)",
        "btn_step_border": "#43a8b4",
        "mpl": {
            "fig_bg": "#1c1b1d",
            "ax_bg": "#262529",
            "primary": "#ffd866",
            "highlight": "#ff6188",
            "success": "#a9dc76",
            "inactive": "#3d3b42",
            "edge": "#d4b055",
            "text": "#fcfcfa",
            "border": "#3d3b42"
        }
    },
    "light": {
        "id": "light",
        "name": "☀️  Nordic Light",
        "bg_main": "#f1f5f9",
        "bg_card": "#ffffff",
        "bg_sidebar": "#e2e8f0",
        "border": "#cbd5e1",
        "text_main": "#0f172a",
        "text_muted": "#475569",
        "accent": "#059669",
        "accent_hover": "#047857",
        "accent_gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #059669, stop:1 #047857)",
        "btn_play_gradient": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #059669, stop:1 #047857)",
        "btn_play_border": "#065f46",
        "btn_pause_gradient": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ea580c, stop:1 #c2410c)",
        "btn_pause_border": "#9a3412",
        "btn_step_gradient": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0d9488, stop:1 #0f766e)",
        "btn_step_border": "#115e59",
        "mpl": {
            "fig_bg": "#f1f5f9",
            "ax_bg": "#ffffff",
            "primary": "#059669",
            "highlight": "#dc2626",
            "success": "#16a34a",
            "inactive": "#e2e8f0",
            "edge": "#047857",
            "text": "#0f172a",
            "border": "#cbd5e1"
        }
    }
}

CURRENT_THEME = "emerald"

def set_current_theme(theme_id):
    global CURRENT_THEME
    if theme_id in THEMES:
        CURRENT_THEME = theme_id

def get_current_theme_id():
    return CURRENT_THEME

def get_theme_qss(theme_id=None):
    tid = theme_id or CURRENT_THEME
    cfg = THEMES.get(tid, THEMES["emerald"])
    return generate_qss(cfg)

def get_mpl_palette(theme_id=None):
    tid = theme_id or CURRENT_THEME
    cfg = THEMES.get(tid, THEMES["emerald"])
    return cfg["mpl"]

def apply_mpl_theme(fig, ax, theme_id=None):
    p = get_mpl_palette(theme_id)
    fig.patch.set_facecolor(p["fig_bg"])
    ax.set_facecolor(p["ax_bg"])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(p["border"])
    ax.spines['bottom'].set_color(p["border"])
    ax.tick_params(colors=p["text"])
