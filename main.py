import os
import sys

if sys.platform == "win32":
    import ctypes
    import importlib.util
    spec = importlib.util.find_spec("PySide6")
    if spec and spec.submodule_search_locations:
        pyside_dir = list(spec.submodule_search_locations)[0]
        if hasattr(os, "add_dll_directory"):
            try:
                os.add_dll_directory(pyside_dir)
            except Exception:
                pass
        kernel32 = ctypes.windll.kernel32
        kernel32.LoadLibraryExW.restype = ctypes.c_void_p
        # 0x00000008 = LOAD_WITH_ALTERED_SEARCH_PATH
        for dll_name in ("Qt6Core.dll", "Qt6Gui.dll", "Qt6Widgets.dll"):
            dll_path = os.path.join(pyside_dir, dll_name)
            if os.path.exists(dll_path):
                kernel32.LoadLibraryExW(dll_path, 0, 8)

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()