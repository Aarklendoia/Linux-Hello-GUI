# Linux Hello – Graphical Configuration Interface

A modern PySide6-based graphical user interface to configure the Linux Hello facial recognition service on KDE and other desktop environments.

## Features

- **Face Enrollment** - Capture and register facial data for authentication
- **PAM Management** - Configure system authentication integration  
- **Advanced Settings** - Adjust recognition thresholds, camera parameters, and performance options
- **Multi-language Support** - Available in 10 languages (AR, DE, EN, ES, FR, IT, JA, PT, RU, ZH_CN)
- **KDE Integration** - Native KDE Plasma support with system theme integration

## Installation

### System Package (Debian/Ubuntu)

```bash
sudo apt-get install linux-hello-gui
```

### From Source

```bash
git clone https://github.com/ebiton/Linux-Hello
cd Linux-Hello-GUI
./install.sh
```

### Development

```bash
pip install -e .
pip install -r requirements.txt
```

## Usage

### Launch Application

```bash
linux-hello-gui
```

### Via KDE Menu

1. Open KDE Application Launcher (usually bottom-left)
2. Search for "Linux Hello" or "Configuration"
3. Click application icon

## User Interface

### 🎥 Face Tab - Facial Recognition Enrollment

- Select camera from available devices
- Live video preview with OpenCV
- Configure number of capture photos (10-100)
- Enroll face with automatic photo capture
- Secure storage in `/etc/linux-hello/faces/`

### 🔐 PAM Tab - Authentication Configuration

- View/edit `/etc/pam.d/linux-hello`
- Three preset security levels:
  - **Strict** - Facial recognition required
  - **Medium** - Facial recognition OR password
  - **Permissive** - Facial recognition optional
- Custom PAM configuration support
- Secure save with sudo escalation

### ⚙️ Settings Tab - Advanced Configuration

**Camera Settings**
- Default camera index
- Video resolution (width/height)

**Recognition Settings**
- Similarity threshold (0.0-1.0)
- Minimum confidence level

**Performance Settings**
- Authentication timeout (1-30 seconds)
- Maximum frames to process

**Logging**
- Log level selection
- Enable/disable logging

## Supported Languages

| Code | Language | Support |
|------|----------|---------|
| en | English | ✓ |
| fr | Français | ✓ |
| de | Deutsch | ✓ |
| es | Español | ✓ |
| it | Italiano | ✓ |
| pt | Português | ✓ |
| ar | العربية | ✓ |
| ru | Русский | ✓ |
| ja | 日本語 | ✓ |
| zh_CN | 简体中文 | ✓ |

Language can be changed via **File → Language** menu.

## Requirements

- Python 3.9+
- PySide6 >= 6.4
- OpenCV (opencv-python) >= 4.8
- Linux system (Ubuntu/Debian recommended)
- KDE Plasma or other compatible desktop environment

## Architecture

```
Linux Hello GUI (PySide6)
├── Face Enrollment Widget (OpenCV)
│   └── → /etc/linux-hello/faces/
├── PAM Manager Widget
│   └── → /etc/pam.d/linux-hello
└── Config Editor Widget
    └── → /etc/linux-hello/config.json
        ↓
    linux-hello daemon
        ↓
    System Authentication (PAM)
```

## Project Structure

```
Linux-Hello-GUI/
├── src/
│   └── linux_hello_gui/
│       ├── main.py              # Application entry point
│       ├── window.py            # Main window with tabs
│       ├── face_enroll.py       # Face enrollment widget
│       ├── pam_manager.py       # PAM configuration widget
│       ├── config_editor.py     # Settings editor widget
│       ├── kde_integration.py   # KDE styling & integration
│       ├── i18n.py              # Internationalization (i18n)
│       ├── camera_widget.py     # Camera utilities
│       └── sudo_helper.py       # Privilege escalation
├── po/
│   ├── linux-hello-gui.pot      # Translation template
│   └── {ar,de,en,es,fr,it,ja,pt,ru,zh_CN}.po
├── debian/
│   ├── control                  # Package metadata
│   ├── rules                    # Build rules
│   ├── postinst                 # Post-installation
│   ├── linux-hello-gui.desktop  # Application launcher
│   └── com.linux-hello.gui.policy # PolicyKit authorization
└── pyproject.toml               # Project configuration
```

## Development

### Setup Development Environment

```bash
pip install -e .
pip install black flake8 pytest
```

### Run Tests

```bash
make test       # Test imports
make lint       # Code style check
make format     # Auto-format code
```

### Make Translations

Edit `.po` files in `po/` directory with:
- `poedit` (graphical editor)
- `gedit` / `vim` (text editors)
- Any translation management tool

Files are automatically compiled to `.mo` on installation.

## Security

- ✅ Secure privilege escalation with sudo
- ✅ Confirmation dialogs before system modifications
- ✅ PolicyKit integration for UI native authorization
- ✅ Protected configuration files
- ✅ Encrypted storage of facial data

## Troubleshooting

### Camera Not Detected

```bash
# Check available cameras
ls /dev/video*

# Test with OpenCV
python3 -c "import cv2; cap = cv2.VideoCapture(0); print('OK' if cap.isOpened() else 'FAIL')"
```

### Permission Errors

Application requires administrator privileges for:
- Modifying `/etc/linux-hello/config.json`
- Writing to `/etc/pam.d/linux-hello`
- Saving facial enrollment data

Use `sudo` or configure passwordless sudo for specific operations.

### Debug Mode

```bash
PYTHONUNBUFFERED=1 linux-hello-gui
```

## Roadmap

- [ ] Dark mode theme support
- [ ] Advanced PAM editor with syntax highlighting
- [ ] Real-time recognition preview
- [ ] Enrollment statistics
- [ ] System integration tests
- [ ] AppImage packaging

## Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing`
3. Commit changes: `git commit -am 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing`
5. Submit pull request

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed guidelines.

## License

See LICENSE file in Linux-Hello project

## Related Projects

- [Linux Hello](https://github.com/ebiton/Linux-Hello) - Main service
- [Linux Hello GUI](https://github.com/ebiton/Linux-Hello/tree/main/Linux-Hello-GUI) - This repository

## Support

- **Issues**: https://github.com/ebiton/Linux-Hello/issues
- **Discussions**: https://github.com/ebiton/Linux-Hello/discussions
- **Documentation**: See [GUIDE.md](GUIDE.md) for user guide

## Acknowledgments

- Built with PySide6 (Qt for Python)
- Uses OpenCV for facial recognition
- KDE Plasma integration
- Inspired by modern Linux security practices

---

**Version**: 1.0.0  
**Status**: Production-Ready  
**Updated**: December 2025
