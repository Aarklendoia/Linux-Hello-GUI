"""Face enrollment widget module."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QLineEdit, QMessageBox, QComboBox, QSpinBox
)
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QPixmap, QImage
import cv2
import numpy as np
import json
import os
import getpass
from .i18n import _


class FaceEnrollWidget(QWidget):
    """Widget for face enrollment functionality."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.recording = False
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel(_("Face Enrollment"))
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Camera selector
        cam_layout = QHBoxLayout()
        cam_layout.addWidget(QLabel(_("Camera:")))
        self.camera_combo = QComboBox()
        self.refresh_cameras()
        cam_layout.addWidget(self.camera_combo)
        refresh_btn = QPushButton(_("Refresh"))
        refresh_btn.clicked.connect(self.refresh_cameras)
        cam_layout.addWidget(refresh_btn)
        layout.addLayout(cam_layout)
        
        # Video preview
        self.video_label = QLabel()
        self.video_label.setMinimumSize(400, 300)
        self.video_label.setStyleSheet("background-color: black; color: white; font-weight: bold;")
        self.video_label.setText(_("Press 'Start Camera' to see preview"))
        self.video_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.video_label)
        
        # Current user info
        current_user = getpass.getuser()
        user_info = QLabel(_("Enrolling face for user: <b>{}</b>").format(current_user))
        layout.addWidget(user_info)
        
        # Number of samples
        samples_layout = QHBoxLayout()
        samples_layout.addWidget(QLabel(_("Number of photos:")))
        self.samples_spinbox = QSpinBox()
        self.samples_spinbox.setMinimum(10)
        self.samples_spinbox.setMaximum(100)
        self.samples_spinbox.setValue(30)
        samples_layout.addWidget(self.samples_spinbox)
        layout.addLayout(samples_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton(_("Start Camera"))
        self.start_btn.clicked.connect(self.start_camera)
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton(_("Stop Camera"))
        self.stop_btn.clicked.connect(self.stop_camera)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)
        
        self.enroll_btn = QPushButton(_("Enroll Face"))
        self.enroll_btn.clicked.connect(self.enroll_face)
        self.enroll_btn.setEnabled(False)
        button_layout.addWidget(self.enroll_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def refresh_cameras(self):
        """Refresh available camera list."""
        self.camera_combo.clear()
        for i in range(5):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                self.camera_combo.addItem(f"Camera {i}", i)
                cap.release()
    
    def start_camera(self):
        """Start camera feed."""
        camera_idx = self.camera_combo.currentData()
        self.cap = cv2.VideoCapture(camera_idx)
        
        if not self.cap.isOpened():
            QMessageBox.warning(self, _("Error"), _("Cannot open camera"))
            return
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.enroll_btn.setEnabled(True)
        self.camera_combo.setEnabled(False)
        self.timer.start(30)
    
    def stop_camera(self):
        """Stop camera feed."""
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None
        
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.enroll_btn.setEnabled(False)
        self.camera_combo.setEnabled(True)
        self.video_label.setText(_("Camera stopped"))
        self.video_label.setPixmap(QPixmap())
    
    def update_frame(self):
        """Update video frame."""
        if not self.cap:
            return
        
        ret, frame = self.cap.read()
        if not ret:
            return
        
        # Resize for display
        frame = cv2.resize(frame, (400, 300))
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert to QImage
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        # Display
        pixmap = QPixmap.fromImage(qt_image)
        self.video_label.setPixmap(pixmap)
    
    def enroll_face(self):
        """Enroll face for current user."""
        current_user = getpass.getuser()
        home_dir = os.path.expanduser("~")
        
        if not self.cap:
            QMessageBox.warning(self, _("Error"), _("Camera is not active"))
            return
        
        # Create enrollment directory in user home
        enroll_dir = os.path.join(home_dir, ".linux-hello", "faces")
        os.makedirs(enroll_dir, exist_ok=True)
        os.chmod(enroll_dir, 0o700)
        
        num_samples = self.samples_spinbox.value()
        captured = 0
        
        self.enroll_btn.setEnabled(False)
        
        while captured < num_samples:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Save frame
            filename = os.path.join(enroll_dir, f"face_{captured:03d}.jpg")
            cv2.imwrite(filename, frame)
            captured += 1
            
            # Update display
            self.video_label.setText(_("Capture {current}/{total}").format(current=captured, total=num_samples))
            self.video_label.update()
        
        self.enroll_btn.setEnabled(True)
        
        if captured == num_samples:
            QMessageBox.information(
                self, 
                _("Success"), 
                _("Face enrolled successfully with {count} photos").format(
                    count=num_samples
                )
            )
        else:
            QMessageBox.warning(
                self, 
                _("Error"), 
                _("Incomplete enrollment: {captured}/{total} photos captured").format(
                    captured=captured, total=num_samples
                )
            )
