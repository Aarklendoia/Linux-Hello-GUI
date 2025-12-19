"""Main entry point for Linux Hello GUI."""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from .window import MainWindow
from .kde_integration import KDEIntegration
from .i18n import setup_gettext, get_available_languages


def main():
    """Main application entry point."""
    # Setup internationalization
    setup_gettext()
    
    app = QApplication(sys.argv)
    
    # Setup KDE integration
    KDEIntegration.apply_kde_style(app)
    KDEIntegration.setup_application_metadata()
    
    # Create and show main window
    win = MainWindow()
    win.show()
    
    sys.exit(app.exec())