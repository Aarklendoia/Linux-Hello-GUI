"""Configuration editor widget."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QSpinBox, QDoubleSpinBox, QMessageBox, QGroupBox, QFormLayout,
    QComboBox, QCheckBox
)
from PySide6.QtCore import Qt
import json
import os
import subprocess
from .i18n import _


class ConfigEditorWidget(QWidget):
    """Widget for editing application configuration."""
    
    def __init__(self):
        super().__init__()
        self.config_path = "/etc/linux-hello/config.json"
        self.config = {}
        self.init_ui()
        self.load_config()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel(_("Linux Hello Settings"))
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Camera settings
        camera_group = QGroupBox(_("Camera Settings"))
        camera_layout = QFormLayout()
        
        self.camera_index = QSpinBox()
        self.camera_index.setMinimum(0)
        self.camera_index.setMaximum(10)
        self.camera_index.setValue(0)
        camera_layout.addRow(_("Default camera index:"), self.camera_index)
        
        self.camera_width = QSpinBox()
        self.camera_width.setMinimum(320)
        self.camera_width.setMaximum(1920)
        self.camera_width.setValue(1280)
        self.camera_width.setSingleStep(10)
        camera_layout.addRow(_("Video width:"), self.camera_width)
        
        self.camera_height = QSpinBox()
        self.camera_height.setMinimum(240)
        self.camera_height.setMaximum(1080)
        self.camera_height.setValue(720)
        self.camera_height.setSingleStep(10)
        camera_layout.addRow(_("Video height:"), self.camera_height)
        
        camera_group.setLayout(camera_layout)
        layout.addWidget(camera_group)
        
        # Recognition settings
        recognition_group = QGroupBox(_("Recognition Settings"))
        recognition_layout = QFormLayout()
        
        self.threshold = QDoubleSpinBox()
        self.threshold.setMinimum(0.0)
        self.threshold.setMaximum(1.0)
        self.threshold.setSingleStep(0.01)
        self.threshold.setValue(0.35)
        recognition_layout.addRow(_("Similarity threshold:"), self.threshold)
        
        self.confidence = QDoubleSpinBox()
        self.confidence.setMinimum(0.0)
        self.confidence.setMaximum(1.0)
        self.confidence.setSingleStep(0.05)
        self.confidence.setValue(0.80)
        recognition_layout.addRow(_("Minimum confidence:"), self.confidence)
        
        recognition_group.setLayout(recognition_layout)
        layout.addWidget(recognition_group)
        
        # Performance settings
        perf_group = QGroupBox(_("Performance Settings"))
        perf_layout = QFormLayout()
        
        self.timeout = QSpinBox()
        self.timeout.setMinimum(1)
        self.timeout.setMaximum(30)
        self.timeout.setValue(5)
        self.timeout.setSuffix(_(" seconds"))
        perf_layout.addRow(_("Timeout:"), self.timeout)
        
        self.max_frames = QSpinBox()
        self.max_frames.setMinimum(1)
        self.max_frames.setMaximum(1000)
        self.max_frames.setValue(100)
        perf_layout.addRow(_("Max frames:"), self.max_frames)
        
        perf_group.setLayout(perf_layout)
        layout.addWidget(perf_group)
        
        # Logging settings
        log_group = QGroupBox(_("Logging"))
        log_layout = QFormLayout()
        
        self.log_level = QComboBox()
        self.log_level.addItem("DEBUG", "DEBUG")
        self.log_level.addItem("INFO", "INFO")
        self.log_level.addItem("WARNING", "WARNING")
        self.log_level.addItem("ERROR", "ERROR")
        self.log_level.addItem("CRITICAL", "CRITICAL")
        log_layout.addRow(_("Log level:"), self.log_level)
        
        self.enable_logging = QCheckBox(_("Enable logging"))
        self.enable_logging.setChecked(True)
        log_layout.addRow(self.enable_logging)
        
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton(_("Save"))
        save_btn.clicked.connect(self.save_config)
        button_layout.addWidget(save_btn)
        
        reload_btn = QPushButton(_("Reload"))
        reload_btn.clicked.connect(self.load_config)
        button_layout.addWidget(reload_btn)
        
        reset_btn = QPushButton(_("Reset to Defaults"))
        reset_btn.clicked.connect(self.reset_to_defaults)
        button_layout.addWidget(reset_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def load_config(self):
        """Load configuration from file."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = self.get_default_config()
            
            # Update UI from config
            self.camera_index.setValue(self.config.get("camera_index", 0))
            self.camera_width.setValue(self.config.get("camera_width", 1280))
            self.camera_height.setValue(self.config.get("camera_height", 720))
            self.threshold.setValue(self.config.get("threshold", 0.35))
            self.confidence.setValue(self.config.get("confidence", 0.80))
            self.timeout.setValue(self.config.get("timeout", 5))
            self.max_frames.setValue(self.config.get("max_frames", 100))
            self.log_level.setCurrentText(self.config.get("log_level", "INFO"))
            self.enable_logging.setChecked(self.config.get("enable_logging", True))
            
        except Exception as e:
            QMessageBox.warning(self, _("Error"), _("Error loading configuration: {error}").format(error=str(e)))
    
    def save_config(self):
        """Save configuration to file."""
        try:
            # Build config from UI
            self.config = {
                "camera_index": self.camera_index.value(),
                "camera_width": self.camera_width.value(),
                "camera_height": self.camera_height.value(),
                "threshold": self.threshold.value(),
                "confidence": self.confidence.value(),
                "timeout": self.timeout.value(),
                "max_frames": self.max_frames.value(),
                "log_level": self.log_level.currentData(),
                "enable_logging": self.enable_logging.isChecked(),
            }
            
            # Ask for confirmation
            reply = QMessageBox.question(
                self,
                _("Confirmation"),
                _("Are you sure you want to save this configuration?\n"
                  "This may require administrator privileges."),
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply != QMessageBox.Yes:
                return
            
            # Create directory if needed
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            # Write config
            config_json = json.dumps(self.config, indent=4)
            
            # Try direct write first
            try:
                with open(self.config_path, 'w') as f:
                    f.write(config_json)
            except PermissionError:
                # Use sudo if needed
                result = subprocess.run(
                    ['sudo', 'tee', self.config_path],
                    input=config_json,
                    text=True,
                    capture_output=True
                )
                
                if result.returncode != 0:
                    raise Exception(result.stderr)
            
            QMessageBox.information(
                self,
                _("Success"),
                _("Configuration saved successfully")
            )
        
        except Exception as e:
            QMessageBox.critical(self, _("Error"), _("Error saving configuration: {error}").format(error=str(e)))
    
    def reset_to_defaults(self):
        """Reset configuration to defaults."""
        reply = QMessageBox.question(
            self,
            _("Confirmation"),
            _("Are you sure you want to reset to default settings?"),
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.config = self.get_default_config()
            self.load_config()
    
    @staticmethod
    def get_default_config():
        """Get default configuration."""
        return {
            "camera_index": 0,
            "camera_width": 1280,
            "camera_height": 720,
            "threshold": 0.35,
            "confidence": 0.80,
            "timeout": 5,
            "max_frames": 100,
            "log_level": "INFO",
            "enable_logging": True,
        }
