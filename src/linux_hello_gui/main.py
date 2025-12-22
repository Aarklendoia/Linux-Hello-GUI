"""Main entry point for Linux Hello GUI."""

import sys
import os
import traceback
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon
from .window import MainWindow
from .i18n import setup_gettext


def main():
    """Main application entry point."""
    try:
        # Setup internationalization
        setup_gettext()
        
        app = QApplication(sys.argv)
        
        # Create and show main window
        win = MainWindow()
        win.show()
        
        sys.exit(app.exec())
    
    except Exception as e:
        # Try to show error dialog, fallback to console
        try:
            app = QApplication.instance() or QApplication(sys.argv)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Linux Hello - Error")
            msg.setText("Error starting Linux Hello GUI:")
            msg.setDetailedText(f"{str(e)}\n\n{traceback.format_exc()}")
            msg.exec()
        except:
            # Fallback to console error
            print(f"❌ Error starting Linux Hello GUI:", file=sys.stderr)
            print(f"{str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
        
        sys.exit(1)


if __name__ == '__main__':
    main()