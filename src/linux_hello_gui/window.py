from PySide6.QtWidgets import QMainWindow, QTabWidget
from .face_enroll import FaceEnrollWidget
from .pam_manager import PamManagerWidget
from .config_editor import ConfigEditorWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Linux Hello – Configuration")
        self.resize(800, 600)

        tabs = QTabWidget()
        tabs.addTab(FaceEnrollWidget(), "Visage")
        tabs.addTab(PamManagerWidget(), "PAM")
        tabs.addTab(ConfigEditorWidget(), "Paramètres")

        self.setCentralWidget(tabs)