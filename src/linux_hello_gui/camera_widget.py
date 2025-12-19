"""Camera utilities and widget module."""

import cv2


class CameraManager:
    """Manages camera operations."""
    
    @staticmethod
    def get_available_cameras(max_index=5):
        """Get list of available cameras."""
        cameras = []
        for i in range(max_index):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cameras.append(i)
                cap.release()
        return cameras
    
    @staticmethod
    def get_camera_properties(camera_index):
        """Get properties of a specific camera."""
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            return None
        
        props = {
            "width": cap.get(cv2.CAP_PROP_FRAME_WIDTH),
            "height": cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
            "fps": cap.get(cv2.CAP_PROP_FPS),
            "brightness": cap.get(cv2.CAP_PROP_BRIGHTNESS),
        }
        
        cap.release()
        return props


class CameraWidget:
    """Widget for camera display and control."""
    pass
