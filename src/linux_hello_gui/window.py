"""Main window widget."""

from PySide6.QtWidgets import (
    QMainWindow, QTabWidget, QStatusBar, QMenuBar, QMenu, 
    QMessageBox, QVBoxLayout, QWidget
)
from PySide6.QtGui import QIcon, QKeySequence
from PySide6.QtCore import Qt
from .face_enroll import FaceEnrollWidget
from .pam_manager import PamManagerWidget
from .config_editor import ConfigEditorWidget
from .kde_integration import IconManager
from .i18n import _, get_available_languages, set_language


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(_("Linux Hello – Configuration"))
        self.setWindowIcon(QIcon.fromTheme("face-recognition"))
        self.resize(900, 700)
        
        # Create central widget
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.face_widget = FaceEnrollWidget()
        self.pam_widget = PamManagerWidget()
        self.config_widget = ConfigEditorWidget()
        
        self.tabs.addTab(self.face_widget, _("👤 Face"))
        self.tabs.addTab(self.pam_widget, _("🔐 PAM"))
        self.tabs.addTab(self.config_widget, _("⚙️ Settings"))
        
        layout.addWidget(self.tabs)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.statusBar().showMessage(_("Ready"))
        
        # Center window on screen
        self.center_window()
    
    def create_menu_bar(self):
        """Create application menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu(_("&File"))
        
        settings_action = file_menu.addAction(_("&Settings"))
        settings_action.triggered.connect(self.show_settings)
        
        file_menu.addSeparator()
        
        quit_action = file_menu.addAction(_("&Quit"))
        quit_action.setShortcut(QKeySequence.Quit)
        quit_action.triggered.connect(self.close)
        
        # Language menu
        lang_menu = menubar.addMenu(_("&Language"))
        languages = get_available_languages()
        
        for lang_code, lang_name in languages.items():
            action = lang_menu.addAction(lang_name)
            action.triggered.connect(lambda checked, code=lang_code: self.change_language(code))
        
        # Help menu
        help_menu = menubar.addMenu(_("&Help"))
        
        about_action = help_menu.addAction(_("&About"))
        about_action.triggered.connect(self.show_about)
        
        about_qt_action = help_menu.addAction(_("About &Qt"))
        about_qt_action.triggered.connect(self.show_about_qt)
    
    def center_window(self):
        """Center window on screen."""
        from PySide6.QtGui import QGuiApplication
        screen = QGuiApplication.primaryScreen()
        if screen:
            geometry = self.frameGeometry()
            center_point = screen.geometry().center()
            geometry.moveCenter(center_point)
            self.move(geometry.topLeft())
    
    def change_language(self, lang_code):
        """Change application language."""
        set_language(lang_code)
        QMessageBox.information(
            self,
            _("Language Changed"),
            _("Please restart the application for language changes to take effect.")
        )
    
    def show_settings(self):
        """Show settings dialog."""
        QMessageBox.information(
            self,
            _("Settings"),
            _("Settings can be modified in the Settings tab.")
        )
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            _("About Linux Hello"),
            _("Linux Hello – Configuration\nVersion 1.0.0\n\n"
              "Graphical interface to configure the Linux Hello "
              "facial recognition service.\n\n"
              "© Linux Hello Contributors")
        )
    
    def show_about_qt(self):
        """Show about Qt dialog."""
        QMessageBox.aboutQt(self, _("About Qt"))