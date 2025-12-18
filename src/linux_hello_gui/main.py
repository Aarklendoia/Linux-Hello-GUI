from PySide6.QtWidgets import QApplication
from .window import MainWindow
import sys

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())