"""PAM (Pluggable Authentication Modules) manager widget."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QTextEdit, QMessageBox, QCheckBox, QGroupBox
)
from PySide6.QtCore import Qt
import subprocess
import os
from .i18n import _


class PamManagerWidget(QWidget):
    """Widget for managing PAM authentication."""
    
    def __init__(self):
        super().__init__()
        self.pam_config_path = "/etc/pam.d/linux-hello"
        self.init_ui()
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
        
        # Authentication Method
        auth_group = QGroupBox(_("Authentication method"))
        auth_layout = QVBoxLayout()
        
        self.auth_face_only = QCheckBox(_("Facial recognition only"))
        self.auth_face_only.setToolTip(_("Face must be recognized to authenticate (highest security)"))
        auth_layout.addWidget(self.auth_face_only)
        
        self.auth_face_with_password = QCheckBox(_("Facial recognition + password fallback"))
        self.auth_face_with_password.setToolTip(_("Use face first, or password if face not recognized"))
        auth_layout.addWidget(self.auth_face_with_password)
        
        # Connect to make them mutually exclusive
        self.auth_face_only.stateChanged.connect(self._on_auth_changed)
        self.auth_face_with_password.stateChanged.connect(self._on_auth_changed)
        
        auth_group.setLayout(auth_layout)
        layout.addWidget(auth_group)
        
        # Options
        options_group = QGroupBox(_("Options"))
        options_layout = QVBoxLayout()
        
        self.option_cache = QCheckBox(_("Cache recognition results"))
        self.option_cache.setChecked(True)
        self.option_cache.setToolTip(_("Faster authentication within 5 minutes"))
        options_layout.addWidget(self.option_cache)
        
        self.option_cache.stateChanged.connect(self.regenerate_config)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Configuration file display
        config_group = QGroupBox(_("Configuration file (/etc/pam.d/linux-hello)"))
        config_layout = QVBoxLayout()
        
        self.config_text = QTextEdit()
        self.config_text.setReadOnly(True)
        self.config_text.setMinimumHeight(200)
        self.config_text.setFontFamily("Monospace")
        config_layout.addWidget(self.config_text)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        reload_btn = QPushButton(_("Reload"))
        reload_btn.clicked.connect(self.load_pam_config)
        button_layout.addWidget(reload_btn)
        
        button_layout.addStretch()
        
        save_btn = QPushButton(_("Save changes"))
        save_btn.setStyleSheet("background-color: #1976d2; color: white;")
        save_btn.clicked.connect(self.on_save_clicked)
        button_layout.addWidget(save_btn)
        
        help_btn = QPushButton(_("Help"))
        help_btn.clicked.connect(self.show_help)
        button_layout.addWidget(help_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def _on_auth_changed(self):
        """Make auth options mutually exclusive."""
        sender = self.sender()
        if sender.isChecked():
            # Uncheck the other one
            if sender == self.auth_face_only:
                self.auth_face_with_password.blockSignals(True)
                self.auth_face_with_password.setChecked(False)
                self.auth_face_with_password.blockSignals(False)
            else:
                self.auth_face_only.blockSignals(True)
                self.auth_face_only.setChecked(False)
                self.auth_face_only.blockSignals(False)
        # Regenerate config after state changes
        self.regenerate_config()
    
    def load_pam_config(self):
        """Load PAM configuration from file."""
        try:
            if os.path.exists(self.pam_config_path):
                with open(self.pam_config_path, 'r') as f:
                    content = f.read()
            else:
                content = _("# PAM configuration not found. Use presets to create it.")
            
            self.config_text.setText(content)
            
            # Parse config to update checkboxes
            self.parse_config(content)
        except PermissionError:
            self.config_text.setText(_("Error: Permission denied to read PAM configuration"))
        except Exception as e:
            self.config_text.setText(_("Error: {error}").format(error=str(e)))
    
    def parse_config(self, content):
        """Parse PAM config to update UI checkboxes."""
        # Detect authentication method from PAM config
        has_pam_exec = "pam_exec.so" in content and "pam_linux_hello.py" in content
        
        # Check if it's face-only (auth required pam_exec, no pam_unix) or face+password
        has_required_pam_exec = "auth required pam_exec.so" in content
        has_pam_unix = "pam_unix.so" in content
        
        # Block signals to avoid triggering regenerate_config multiple times
        self.auth_face_only.blockSignals(True)
        self.auth_face_with_password.blockSignals(True)
        self.option_cache.blockSignals(True)
        
        try:
            # Detect which auth method is configured
            if has_pam_exec and has_required_pam_exec and not has_pam_unix:
                # Face-only (Strict)
                self.auth_face_only.setChecked(True)
                self.auth_face_with_password.setChecked(False)
            elif has_pam_exec and has_pam_unix:
                # Face + password fallback
                self.auth_face_only.setChecked(False)
                self.auth_face_with_password.setChecked(True)
            else:
                # No PAM config or custom
                self.auth_face_only.setChecked(False)
                self.auth_face_with_password.setChecked(False)
            
            # Check for cache (if "cache" mentioned in config)
            self.option_cache.setChecked("cache" in content.lower())
        finally:
            self.auth_face_only.blockSignals(False)
            self.auth_face_with_password.blockSignals(False)
            self.option_cache.blockSignals(False)
    
    def regenerate_config(self):
        """Regenerate PAM config based on current checkbox state."""
        config = self.generate_pam_config()
        self.config_text.setText(config)
    
    def generate_pam_config(self):
        """Generate PAM configuration based on selected options."""
        lines = []
        
        # Determine which authentication method is selected
        face_only = self.auth_face_only.isChecked()
        face_with_password = self.auth_face_with_password.isChecked()
        
        if not face_only and not face_with_password:
            # No method selected - just show standard unix auth
            lines.append("# No facial recognition configured")
            lines.append("")
            lines.append("auth required pam_unix.so")
            lines.append("account required pam_unix.so")
            lines.append("password required pam_unix.so sha512 shadow nullok try_first_pass use_authtok")
            lines.append("session required pam_unix.so")
            self.config_text.setText("\n".join(lines))
            return "\n".join(lines)
        
        # Generate header comment
        if face_only:
            mode = "FACE-ONLY"
            description = "Facial recognition required, password NOT allowed"
        else:
            mode = "FACE+PASSWORD"
            description = "Facial recognition OR password (either one works)"
        
        lines.append(f"# Linux Hello PAM Configuration - {mode} mode")
        lines.append(f"# {description}")
        lines.append("")
        
        # Generate PAM rules
        if face_only:
            # FACE-ONLY: face required, no password
            lines.append("auth required pam_exec.so quiet expose_authtok /usr/lib/linux-hello/pam_linux_hello.py")
            lines.append("auth required pam_deny.so")
            lines.append("account required pam_permit.so")
            lines.append("password required pam_exec.so quiet expose_authtok /usr/lib/linux-hello/pam_linux_hello.py")
            lines.append("session required pam_permit.so")
        else:
            # FACE+PASSWORD: face sufficient (can skip password), but password as fallback
            lines.append("auth sufficient pam_exec.so quiet expose_authtok /usr/lib/linux-hello/pam_linux_hello.py")
            lines.append("auth required pam_unix.so nullok try_first_pass")
            lines.append("account required pam_unix.so")
            lines.append("password required pam_unix.so sha512 shadow nullok try_first_pass use_authtok")
            lines.append("session required pam_unix.so")
        
        lines.append("")
        
        return "\n".join(lines)
    
    def on_save_clicked(self):
        """Handle save button click - confirm before saving."""
        content = self.config_text.toPlainText().strip()
        
        # Validate that content has actual PAM configuration lines
        # (not just comments or whitespace)
        has_auth_line = "auth" in content
        has_account_line = "account" in content
        has_session_line = "session" in content
        
        # At minimum, we need some auth rules
        if not content or not has_auth_line:
            QMessageBox.warning(
                self,
                _("Invalid configuration"),
                _("PAM configuration must contain at least one 'auth' line.")
            )
            return
        
        self.save_pam_config(content)
    
    def save_pam_config(self, content=None):
        """Save PAM configuration to file."""
        try:
            if content is None:
                content = self.config_text.toPlainText()
            
            # Ask for confirmation
            reply = QMessageBox.question(
                self,
                _("Confirmation"),
                _("This will modify system PAM configuration.\n"
                  "Enter your administrator password when prompted."),
                QMessageBox.Ok | QMessageBox.Cancel
            )
            
            if reply != QMessageBox.Ok:
                return
            
            # Create temp file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pam') as tmp:
                tmp.write(content)
                tmp_path = tmp.name
            
            try:
                # Save to /etc/pam.d/linux-hello
                result = subprocess.run(
                    ['pkexec', 'cp', tmp_path, self.pam_config_path],
                    capture_output=True,
                    timeout=30
                )
                
                if result.returncode != 0:
                    result = subprocess.run(
                        ['sudo', 'cp', tmp_path, self.pam_config_path],
                        capture_output=True,
                        timeout=30
                    )
                
                if result.returncode != 0:
                    error_msg = result.stderr.decode('utf-8', errors='ignore') if result.stderr else "Unknown error"
                    QMessageBox.critical(
                        self,
                        _("Error"),
                        _("Failed to save PAM configuration:\n{error}").format(error=error_msg)
                    )
                    return
                
                # Verify file was written correctly
                if os.path.exists(self.pam_config_path):
                    with open(self.pam_config_path, 'r') as f:
                        saved_content = f.read().strip()
                    
                    if saved_content == content.strip():
                        QMessageBox.information(
                            self,
                            _("Success"),
                            _("PAM configuration saved successfully!\n"
                              "Changes take effect immediately.")
                        )
                        self.load_pam_config()
                    else:
                        QMessageBox.warning(
                            self,
                            _("Error"),
                            _("Configuration was not saved correctly.\n"
                              "File content does not match.")
                        )
                else:
                    QMessageBox.warning(
                        self,
                        _("Error"),
                        _("PAM configuration file was not created.")
                    )
            finally:
                # Clean up temp file
                try:
                    os.remove(tmp_path)
                except:
                    pass
        
        except subprocess.TimeoutExpired:
            QMessageBox.critical(self, _("Error"), _("Operation timed out. No administrator password provided?"))
        except Exception as e:
            QMessageBox.critical(self, _("Error"), _("Error: {error}").format(error=str(e)))
    
    def show_help(self):
        """Show help dialog."""
        help_text = _("""
<b>PAM Configuration Help</b>

<b>Authentication Method:</b>
• <b>Facial recognition only:</b> Your face MUST be recognized to authenticate (highest security)
• <b>Facial recognition + password fallback:</b> Use your face first, or your password if face is not recognized (balanced security & convenience)

<b>Options:</b>
• <b>Cache recognition results:</b> Faster authentication by remembering your face for up to 5 minutes

<b>How it works:</b>
When you select a method, the PAM configuration is generated and shown below.
Click "Save changes" to apply it to your system (requires administrator password).

The configuration takes effect immediately for login and sudo commands.
""")
        
        msg = QMessageBox(self)
        msg.setWindowTitle(_("Help"))
        msg.setText(help_text)
        msg.setIcon(QMessageBox.Information)
        msg.exec()
