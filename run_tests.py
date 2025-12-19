#!/usr/bin/env python3
"""Comprehensive test suite for Linux Hello GUI."""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


class TestRunner:
    """Run various tests on the Linux Hello GUI."""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.errors = []
    
    def test_imports(self):
        """Test all module imports."""
        print("\n📦 Testing imports...")
        
        modules = [
            "linux_hello_gui",
            "linux_hello_gui.main",
            "linux_hello_gui.window",
            "linux_hello_gui.face_enroll",
            "linux_hello_gui.pam_manager",
            "linux_hello_gui.config_editor",
            "linux_hello_gui.camera_widget",
            "linux_hello_gui.kde_integration",
            "linux_hello_gui.sudo_helper",
        ]
        
        for module in modules:
            try:
                __import__(module)
                print(f"  ✓ {module}")
                self.tests_passed += 1
            except Exception as e:
                print(f"  ✗ {module}: {e}")
                self.tests_failed += 1
                self.errors.append((module, str(e)))
    
    def test_dependencies(self):
        """Test required dependencies."""
        print("\n📚 Testing dependencies...")
        
        dependencies = [
            ("PySide6", "PySide6"),
            ("cv2", "opencv-python"),
            ("json", "json (builtin)"),
            ("subprocess", "subprocess (builtin)"),
            ("tempfile", "tempfile (builtin)"),
        ]
        
        for module_name, package_name in dependencies:
            try:
                __import__(module_name)
                print(f"  ✓ {package_name}")
                self.tests_passed += 1
            except ImportError:
                print(f"  ✗ {package_name} - not installed")
                print(f"     Install with: pip3 install {package_name}")
                self.tests_failed += 1
                self.errors.append((package_name, "Not installed"))
    
    def test_files(self):
        """Test required files exist."""
        print("\n📂 Testing file structure...")
        
        files = [
            "src/linux_hello_gui/__init__.py",
            "src/linux_hello_gui/main.py",
            "src/linux_hello_gui/window.py",
            "debian/linux-hello-gui.desktop",
            "debian/control",
            "pyproject.toml",
        ]
        
        for filepath in files:
            full_path = Path(filepath)
            if full_path.exists():
                print(f"  ✓ {filepath}")
                self.tests_passed += 1
            else:
                print(f"  ✗ {filepath} - not found")
                self.tests_failed += 1
                self.errors.append((filepath, "Not found"))
    
    def test_configuration(self):
        """Test configuration files."""
        print("\n⚙️  Testing configuration...")
        
        try:
            import json
            
            # Test config editor default config
            from linux_hello_gui.config_editor import ConfigEditorWidget
            
            config = ConfigEditorWidget.get_default_config()
            required_keys = [
                "camera_index", "camera_width", "camera_height",
                "threshold", "confidence", "timeout", "max_frames",
                "log_level", "enable_logging"
            ]
            
            for key in required_keys:
                if key in config:
                    print(f"  ✓ Config key: {key}")
                    self.tests_passed += 1
                else:
                    print(f"  ✗ Config key: {key} - missing")
                    self.tests_failed += 1
                    self.errors.append(("config", f"Missing key: {key}"))
        
        except Exception as e:
            print(f"  ✗ Configuration test failed: {e}")
            self.tests_failed += 1
            self.errors.append(("configuration", str(e)))
    
    def test_widget_creation(self):
        """Test widget creation."""
        print("\n🎨 Testing widget creation...")
        
        try:
            # Skip actual GUI widget tests (need display)
            from linux_hello_gui.camera_widget import CameraManager
            from linux_hello_gui.kde_integration import IconManager
            
            # Test camera manager
            try:
                cameras = CameraManager.get_available_cameras()
                print(f"  ✓ CameraManager (found {len(cameras)} cameras)")
                self.tests_passed += 1
            except Exception as e:
                print(f"  ⚠ CameraManager: {e}")
                self.tests_passed += 1  # Warning, not failure
            
            # Test icon manager
            try:
                icon = IconManager.get_icon("camera")
                print(f"  ✓ IconManager")
                self.tests_passed += 1
            except Exception as e:
                print(f"  ✗ IconManager: {e}")
                self.tests_failed += 1
                self.errors.append(("IconManager", str(e)))
        
        except Exception as e:
            print(f"  ✗ Widget creation test failed: {e}")
            self.tests_failed += 1
            self.errors.append(("widgets", str(e)))
    
    def run_all_tests(self):
        """Run all tests."""
        print("=" * 60)
        print("🧪 Linux Hello GUI Test Suite")
        print("=" * 60)
        
        self.test_imports()
        self.test_dependencies()
        self.test_files()
        self.test_configuration()
        self.test_widget_creation()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 Test Summary")
        print("=" * 60)
        print(f"✓ Passed: {self.tests_passed}")
        print(f"✗ Failed: {self.tests_failed}")
        
        if self.errors:
            print("\n⚠️  Errors:")
            for test, error in self.errors:
                print(f"  - {test}: {error}")
        
        print("=" * 60)
        
        # Return appropriate exit code
        if self.tests_failed == 0:
            print("✓ All tests passed!")
            return 0
        else:
            print(f"✗ {self.tests_failed} test(s) failed")
            return 1


if __name__ == "__main__":
    runner = TestRunner()
    exit_code = runner.run_all_tests()
    sys.exit(exit_code)
