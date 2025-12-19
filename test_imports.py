#!/usr/bin/env python3
"""Simple test script to validate GUI components."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from linux_hello_gui import main
        print("✓ main module")
    except Exception as e:
        print(f"✗ main module: {e}")
        return False
    
    try:
        from linux_hello_gui.window import MainWindow
        print("✓ MainWindow")
    except Exception as e:
        print(f"✗ MainWindow: {e}")
        return False
    
    try:
        from linux_hello_gui.face_enroll import FaceEnrollWidget
        print("✓ FaceEnrollWidget")
    except Exception as e:
        print(f"✗ FaceEnrollWidget: {e}")
        return False
    
    try:
        from linux_hello_gui.pam_manager import PamManagerWidget
        print("✓ PamManagerWidget")
    except Exception as e:
        print(f"✗ PamManagerWidget: {e}")
        return False
    
    try:
        from linux_hello_gui.config_editor import ConfigEditorWidget
        print("✓ ConfigEditorWidget")
    except Exception as e:
        print(f"✗ ConfigEditorWidget: {e}")
        return False
    
    try:
        from linux_hello_gui.kde_integration import KDEIntegration
        print("✓ KDEIntegration")
    except Exception as e:
        print(f"✗ KDEIntegration: {e}")
        return False
    
    print("\n✓ All imports successful!")
    return True


if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
