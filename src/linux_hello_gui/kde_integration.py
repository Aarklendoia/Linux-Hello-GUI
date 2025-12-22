"""KDE integration and styling module."""

from PySide6.QtWidgets import QApplication, QStyle
from PySide6.QtGui import QIcon, QColor, QFont
from PySide6.QtCore import QSize
import sys


class KDEIntegration:
    """Handle KDE-specific integration and styling."""
    
    @staticmethod
    def apply_kde_style(app: QApplication):
        """Apply KDE-compatible style to the application."""
        # Try to use KDE style if available
        kde_style = QApplication.style()
        if kde_style:
            app.setStyle(kde_style)
    
    @staticmethod
    def setup_application_metadata():
        """Setup application metadata for KDE integration."""
        app = QApplication.instance()
        if app:
            app.setApplicationName("Linux Hello Configuration")
            app.setApplicationVersion("1.0.0")
            app.setApplicationDisplayName("Configuration Linux Hello")
            try:
                app.setApplicationAuthor("Linux Hello Contributors")
            except AttributeError:
                # PySide6 may not have setApplicationAuthor
                pass
            try:
                app.setWindowIcon(QIcon.fromTheme("face-recognition"))
            except:
                pass
    
    @staticmethod
    def get_kde_color(color_name: str) -> QColor:
        """Get KDE palette color by name."""
        palette = QApplication.palette()
        
        color_map = {
            "window": palette.color(palette.Window),
            "button": palette.color(palette.Button),
            "text": palette.color(palette.Text),
            "base": palette.color(palette.Base),
            "highlight": palette.color(palette.Highlight),
            "alternate": palette.color(palette.AlternateBase),
        }
        
        return color_map.get(color_name, palette.color(palette.Window))
    
    @staticmethod
    def create_default_font(size_adjustment=0):
        """Create a KDE-compatible font."""
        font = QApplication.font()
        if size_adjustment != 0:
            font.setPointSize(font.pointSize() + size_adjustment)
        return font


class IconManager:
    """Manage application icons with KDE theme fallbacks."""
    
    # Standard icon names for KDE
    ICONS = {
        "camera": "camera-photo",
        "config": "preferences-system",
        "user": "user-identity",
        "lock": "security-high",
        "save": "document-save",
        "reset": "edit-undo",
        "refresh": "view-refresh",
        "info": "dialog-information",
        "warning": "dialog-warning",
        "error": "dialog-error",
        "success": "dialog-ok",
    }
    
    @staticmethod
    def get_icon(icon_name: str) -> QIcon:
        """Get an icon with KDE theme fallback."""
        kde_name = IconManager.ICONS.get(icon_name, icon_name)
        icon = QIcon.fromTheme(kde_name)
        
        if icon.isNull():
            # Fallback if theme icon not found
            return QIcon()
        
        return icon
    
    @staticmethod
    def set_button_icon(button, icon_name: str):
        """Set button icon with KDE integration."""
        icon = IconManager.get_icon(icon_name)
        if not icon.isNull():
            button.setIcon(icon)
            button.setIconSize(QSize(24, 24))
