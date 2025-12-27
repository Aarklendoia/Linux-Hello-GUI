"""User-friendly main window widget with live camera preview."""

from PySide6.QtWidgets import (
    QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QLabel, QMessageBox
)
from PySide6.QtGui import QIcon, QFont, QPixmap, QImage
from PySide6.QtCore import Qt, QProcess, QTimer
import cv2
import getpass
import os
from pathlib import Path
from .pam_manager import PamManagerWidget
from .i18n import _


class MainWindow(QMainWindow):
    """User-friendly main application window with live preview."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(_("Linux Hello"))
        
        # Load application icon
        icon = self._load_app_icon()
        if icon:
            self.setWindowIcon(icon)
        else:
            # Fallback to system theme icon
            self.setWindowIcon(QIcon.fromTheme("face-recognition"))
        
        self.resize(700, 600)
        
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        
        # Create central widget with tabs
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Tab 1: Face (main interface)
        self.tabs.addTab(self.create_face_tab(), _("Face"))
        
        # Tab 2: Settings (PAM config)
        self.pam_widget = PamManagerWidget()
        self.tabs.addTab(self.pam_widget, _("Settings"))
        
        layout.addWidget(self.tabs)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # Status bar
        self.statusBar().showMessage(_("Ready"))
        
        # Start camera on init
        self.start_camera()
    
    def create_face_tab(self):
        """Create user-friendly face tab with live preview."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Top: Current user info and profile status
        header_layout = QHBoxLayout()
        current_user = getpass.getuser()
        user_label = QLabel(f"<b>{_('User')}:</b> {current_user}")
        header_layout.addWidget(user_label)
        header_layout.addStretch()
        
        refresh_status_btn = QPushButton(_("Refresh"))
        refresh_status_btn.setMaximumWidth(80)
        refresh_status_btn.clicked.connect(self.refresh_profile_status)
        header_layout.addWidget(refresh_status_btn)
        
        layout.addLayout(header_layout)
        
        # Middle: Live camera preview (always visible)
        self.video_label = QLabel()
        self.video_label.setMinimumSize(600, 400)
        self.video_label.setStyleSheet("background-color: black; border: 2px solid #666;")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setText(_("Initializing camera..."))
        layout.addWidget(self.video_label)
        
        # Bottom: Action buttons (simple workflow)
        button_layout = QVBoxLayout()
        
        # Main action: Register face with status indicator on button
        self.enroll_btn = QPushButton()
        self.enroll_btn.setMinimumHeight(60)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.enroll_btn.setFont(font)
        self.enroll_btn.setStyleSheet("background-color: #1976d2; color: white; border-radius: 5px;")
        self.enroll_btn.clicked.connect(self.start_enrollment_workflow)
        button_layout.addWidget(self.enroll_btn)
        
        # Secondary actions
        secondary_layout = QHBoxLayout()
        
        test_btn = QPushButton(_("Test"))
        test_btn.clicked.connect(self.run_test)
        secondary_layout.addWidget(test_btn)
        
        remove_btn = QPushButton(_("Remove"))
        remove_btn.setStyleSheet("color: #d32f2f;")
        remove_btn.clicked.connect(self.run_remove)
        secondary_layout.addWidget(remove_btn)
        
        doctor_btn = QPushButton(_("Diagnostics"))
        doctor_btn.clicked.connect(self.run_doctor)
        secondary_layout.addWidget(doctor_btn)
        
        button_layout.addLayout(secondary_layout)
        layout.addLayout(button_layout)
        
        # Check profile status on load
        self.refresh_profile_status()
        
        return widget
    
    def start_camera(self):
        """Start the camera and begin live preview."""
        if not self.cap:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                self.video_label.setText(_("Camera not available"))
                self.statusBar().showMessage(_("Camera error"))
                return
            
            # Start timer for frame updates
            self.timer.start(33)  # ~30 fps
            self.statusBar().showMessage(_("Camera ready"))
    
    def stop_camera(self):
        """Stop camera and live preview."""
        if self.timer.isActive():
            self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None
    
    def update_frame(self):
        """Update video frame from camera."""
        if not self.cap or not self.cap.isOpened():
            return
        
        ret, frame = self.cap.read()
        if not ret:
            return
        
        # Resize and convert
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        
        # Display
        self.video_label.setPixmap(pixmap.scaledToWidth(600, Qt.SmoothTransformation))
    
    def refresh_profile_status(self):
        """Check and display profile status for current user."""
        current_user = getpass.getuser()
        home_dir = os.path.expanduser("~")
        faces_dir = os.path.join(home_dir, ".linux-hello", "faces")
        face_file = os.path.join(faces_dir, f"{current_user}.npy")
        
        if os.path.exists(face_file):
            self.enroll_btn.setText("✓ " + _("Register Face"))
            self.enroll_btn.setStyleSheet("background-color: #388e3c; color: white; border-radius: 5px;")
        else:
            self.enroll_btn.setText("✗ " + _("Register Face"))
            self.enroll_btn.setStyleSheet("background-color: #d32f2f; color: white; border-radius: 5px;")
    
    def start_enrollment_workflow(self):
        """Start the face enrollment workflow with camera preview."""
        # Show dialog to start enrollment
        reply = QMessageBox.question(
            self,
            _("Face Registration"),
            _("Ready to register your face?\n\n"
              "Make sure you have good lighting and"
              " position your face in the center.\n\n"
              "The system will capture 30 photos."),
            QMessageBox.Ok | QMessageBox.Cancel
        )
        
        if reply == QMessageBox.Ok:
            self.perform_enrollment()
    
    def perform_enrollment(self):
        """Perform face enrollment via CLI command."""
        self.statusBar().showMessage(_("Enrolling..."))
        
        try:
            # Close camera to avoid conflicts with daemon
            self.stop_camera()
            
            # Run enrollment via CLI
            process = QProcess(self)
            process.start("hello", ["enroll"])
            process.waitForFinished(120000)  # 2 minutes timeout
            
            # Restart camera
            self.start_camera()
            
            if process.exitCode() == 0:
                self.refresh_profile_status()
                self.statusBar().showMessage(_("✓ Face registered successfully!"))
            else:
                self.statusBar().showMessage(_("✗ Enrollment failed"))
            
        except Exception as e:
            self.statusBar().showMessage(_("Error: {error}").format(error=str(e)))
            self.start_camera()
    
    def run_test(self):
        """Run face recognition test."""
        self.statusBar().showMessage(_("Testing recognition..."))
        
        try:
            # Close camera to avoid conflicts with daemon
            self.stop_camera()
            
            # Run test
            process = QProcess(self)
            process.start("hello", ["test"])
            process.waitForFinished(30000)
            
            # Restart camera
            self.start_camera()
            
            if process.exitCode() == 0:
                self.statusBar().showMessage(_("✓ Face recognized!"))
            else:
                self.statusBar().showMessage(_("✗ Face not recognized"))
            
        except Exception as e:
            self.statusBar().showMessage(_("Error: {error}").format(error=str(e)))
            self.start_camera()
    
    def run_remove(self):
        """Remove face registration."""
        current_user = getpass.getuser()
        result = QMessageBox.question(
            self,
            _("Remove Profile"),
            _("Remove face registration for '{user}'?").format(user=current_user),
            QMessageBox.Yes | QMessageBox.No
        )
        
        if result == QMessageBox.Yes:
            try:
                # Close camera to avoid conflicts
                self.stop_camera()
                
                process = QProcess(self)
                process.start("hello", ["remove", current_user])
                process.waitForFinished(5000)
                
                # Restart camera
                self.start_camera()
                
                if process.exitCode() == 0:
                    self.refresh_profile_status()
                    self.statusBar().showMessage(_("Profile removed"))
                else:
                    self.statusBar().showMessage(_("Error removing profile"))
            except Exception as e:
                self.statusBar().showMessage(_("Error: {error}").format(error=str(e)))
                self.start_camera()
    
    def run_doctor(self):
        """Run system diagnostics."""
        self.statusBar().showMessage(_("Running diagnostics..."))
        
        try:
            # Close camera to avoid conflicts
            self.stop_camera()
            
            process = QProcess(self)
            process.start("hello", ["doctor"])
            process.waitForFinished(30000)
            
            # Restart camera
            self.start_camera()
            
            if process.exitCode() == 0:
                self.statusBar().showMessage(_("✓ All systems operational"))
            else:
                self.statusBar().showMessage(_("✗ Some issues detected"))
            
        except Exception as e:
            self.statusBar().showMessage(_("Error: {error}").format(error=str(e)))
            self.start_camera()
    
    def _load_app_icon(self):
        """Load application icon from various possible locations."""
        icon_paths = [
            # Development location
            Path(__file__).parent.parent.parent / "icon.png",
            # Installed location
            Path("/usr/share/linux-hello-gui/icon.png"),
            # Alternative installed location
            Path("/usr/share/pixmaps/linux-hello-gui.png"),
            # Current directory
            Path("icon.png"),
        ]
        
        for icon_path in icon_paths:
            if icon_path.exists():
                try:
                    return QIcon(str(icon_path))
                except Exception:
                    continue
        
        # No icon found
        return None
    
    def closeEvent(self, event):
        """Clean up when closing."""
        self.stop_camera()
        event.accept()
