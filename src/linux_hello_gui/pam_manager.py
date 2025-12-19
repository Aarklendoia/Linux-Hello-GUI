"""PAM (Pluggable Authentication Modules) manager widget."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QTextEdit, QMessageBox, QCheckBox, QGroupBox, QComboBox
)
from PySide6.QtCore import Qt
import subprocess
import os
from .i18n import _


class PamManagerWidget(QWidget):
    """Widget for managing PAM authentication."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.pam_config_path = "/etc/pam.d/linux-hello"
        self.load_pam_config()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel(_("PAM Configuration (Authentication)"))
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Status info
        info_label = QLabel(
            _("PAM (Pluggable Authentication Modules) allows using "
              "facial recognition for system authentication.")
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Configuration file display
        config_group = QGroupBox(_("PAM Configuration"))
        config_layout = QVBoxLayout()
        
        self.config_text = QTextEdit()
        self.config_text.setReadOnly(True)
        self.config_text.setMinimumHeight(200)
        config_layout.addWidget(self.config_text)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Preset configurations
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel(_("Preset configuration:")))
        self.preset_combo = QComboBox()
        self.preset_combo.addItem(_("Strict (facial recognition required)"), "strict")
        self.preset_combo.addItem(_("Medium (facial recognition + password)"), "medium")
        self.preset_combo.addItem(_("Permissive (facial recognition optional)"), "permissive")
        preset_layout.addWidget(self.preset_combo)
        
        apply_preset_btn = QPushButton(_("Apply"))
        apply_preset_btn.clicked.connect(self.apply_preset)
        preset_layout.addWidget(apply_preset_btn)
        layout.addLayout(preset_layout)
        
        # Options
        options_group = QGroupBox(_("Options"))
        options_layout = QVBoxLayout()
        
        self.require_face_check = QCheckBox(_("Facial recognition required"))
        options_layout.addWidget(self.require_face_check)
        
        self.allow_password_check = QCheckBox(_("Allow password as fallback"))
        self.allow_password_check.setChecked(True)
        options_layout.addWidget(self.allow_password_check)
        
        self.cache_check = QCheckBox(_("Cache results"))
        self.cache_check.setChecked(True)
        options_layout.addWidget(self.cache_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton(_("Save Configuration"))
        save_btn.clicked.connect(self.save_pam_config)
        button_layout.addWidget(save_btn)
        
        reload_btn = QPushButton(_("Reload from Disk"))
        reload_btn.clicked.connect(self.load_pam_config)
        button_layout.addWidget(reload_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def load_pam_config(self):
        """Load PAM configuration from file."""
        try:
            if os.path.exists(self.pam_config_path):
                with open(self.pam_config_path, 'r') as f:
                    content = f.read()
            else:
                content = _("# PAM configuration not found")
            
            self.config_text.setText(content)
        except PermissionError:
            self.config_text.setText(_("Error: Permission denied to read PAM configuration"))
        except Exception as e:
            self.config_text.setText(_("Error: {error}").format(error=str(e)))
    
    def apply_preset(self):
        """Apply a preset PAM configuration."""
        preset = self.preset_combo.currentData()
        
        if preset == "strict":
            config = """# PAM configuration for Linux Hello - STRICT mode
# Require facial recognition only

auth required pam_unix.so nullok try_first_pass
auth required pam_linux_hello.so
account required pam_unix.so
password required pam_unix.so sha512 shadow nullok try_first_pass use_authtok
session required pam_unix.so
"""
            self.require_face_check.setChecked(True)
            self.allow_password_check.setChecked(False)
            
        elif preset == "medium":
            config = """# PAM configuration for Linux Hello - MEDIUM mode
# Require facial recognition OR password

auth sufficient pam_linux_hello.so
auth required pam_unix.so nullok try_first_pass
account required pam_unix.so
password required pam_unix.so sha512 shadow nullok try_first_pass use_authtok
session required pam_unix.so
"""
            self.require_face_check.setChecked(True)
            self.allow_password_check.setChecked(True)
            
        elif preset == "permissive":
            config = """# PAM configuration for Linux Hello - PERMISSIVE mode
# Facial recognition optional

auth optional pam_linux_hello.so
auth required pam_unix.so nullok try_first_pass
account required pam_unix.so
password required pam_unix.so sha512 shadow nullok try_first_pass use_authtok
session required pam_unix.so
"""
            self.require_face_check.setChecked(False)
            self.allow_password_check.setChecked(True)
        
        self.config_text.setText(config)
        QMessageBox.information(self, _("Info"), _("Configuration '{preset}' applied").format(preset=preset))
    
    def save_pam_config(self):
        """Save PAM configuration to file."""
        try:
            content = self.config_text.toPlainText()
            
            # Ask for confirmation
            reply = QMessageBox.question(
                self,
                _("Confirmation"),
                _("Are you sure you want to modify the PAM configuration?\n"
                  "This requires administrator privileges."),
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply != QMessageBox.Yes:
                return
            
            # Write with sudo
            result = subprocess.run(
                ['sudo', 'tee', self.pam_config_path],
                input=content,
                text=True,
                capture_output=True
            )
            
            if result.returncode == 0:
                QMessageBox.information(
                    self,
                    _("Success"),
                    _("PAM configuration saved successfully")
                )
                self.load_pam_config()
            else:
                QMessageBox.warning(
                    self,
                    _("Error"),
                    _("Error saving configuration: {error}").format(error=result.stderr)
                )
        
        except Exception as e:
            QMessageBox.critical(self, _("Error"), _("Error: {error}").format(error=str(e)))
