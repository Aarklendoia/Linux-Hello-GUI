# Guide de Développement – Linux Hello GUI

## Structure du Projet

```
Linux-Hello-GUI/
├── src/
│   └── linux_hello_gui/
│       ├── __init__.py           # Package initialization
│       ├── main.py               # Application entry point
│       ├── window.py             # Main window (tabs)
│       ├── face_enroll.py        # Face enrollment widget
│       ├── pam_manager.py        # PAM configuration widget
│       ├── config_editor.py      # Settings editor widget
│       ├── camera_widget.py      # Camera utilities
│       ├── kde_integration.py    # KDE styling & icons
│       └── sudo_helper.py        # Privilege escalation
├── debian/
│   ├── control                   # Debian package metadata
│   ├── linux-hello-gui.desktop   # Application launcher
│   ├── com.linux-hello.gui.policy # PolicyKit rules
│   └── install
├── pyproject.toml                # Project configuration
├── requirements.txt              # Python dependencies
├── Makefile                      # Build automation
├── install.sh                    # Installation script
└── README.md                     # Documentation
```

## Prérequis Développement

### Système

```bash
# Ubuntu/Debian
sudo apt-get install python3-dev python3-pip
sudo apt-get install libpyside6-dev
sudo apt-get install libopencv-dev python3-opencv

# Fedora/CentOS
sudo dnf install python3-devel
sudo dnf install python3-pyside6
sudo dnf install python3-opencv
```

### Python

```bash
pip3 install -r requirements.txt
pip3 install -e .
```

## Architecture des Widgets

### FaceEnrollWidget
- Gère la capture vidéo de la caméra
- Permet l'enregistrement de multiples photos du visage
- Intègre OpenCV pour le traitement vidéo
- Stocke les images dans `/etc/linux-hello/faces/<username>/`

### PamManagerWidget
- Affiche et édite `/etc/pam.d/linux-hello`
- Propose des configurations prédéfinies (strict, medium, permissive)
- Requiert `sudo` pour les modifications

### ConfigEditorWidget
- Gère la configuration JSON (`/etc/linux-hello/config.json`)
- Permet d'ajuster:
  - Index et résolution caméra
  - Seuils de reconnaissance
  - Paramètres de performance
  - Options de journalisation

## Flux de Données

```
┌─────────────────────────────────────────┐
│         GUI Application (PySide6)       │
├─────────────────────────────────────────┤
│                                         │
│  ┌────────────────────────────────┐    │
│  │   FaceEnrollWidget             │    │
│  │  (OpenCV camera capture)       │    │
│  └────────────────────────────────┘    │
│           ↓                             │
│  /etc/linux-hello/faces/<user>/        │
│           ↓                             │
│  linux-hello (daemon/service)          │
│  Utilisé par: PAM, CLI, authentification
│                                         │
│  ┌────────────────────────────────┐    │
│  │   ConfigEditorWidget           │    │
│  │  (JSON config editor)          │    │
│  └────────────────────────────────┘    │
│           ↓                             │
│  /etc/linux-hello/config.json          │
│                                         │
│  ┌────────────────────────────────┐    │
│  │   PamManagerWidget             │    │
│  │  (PAM configuration)           │    │
│  └────────────────────────────────┘    │
│           ↓                             │
│  /etc/pam.d/linux-hello                │
└─────────────────────────────────────────┘
```

## Développement Local

### Installation en mode développement

```bash
pip3 install -e .
pip3 install -d .  # Install dev dependencies
```

### Lancer l'application

```bash
# Méthode 1
make run

# Méthode 2
python3 -m linux_hello_gui.main

# Méthode 3
linux-hello-gui
```

### Tests

```bash
make test       # Test des imports
make lint       # Vérification PEP8
make format     # Formatage automatique
```

## Intégration KDE

### Thème et Style
- Utilise `KDEIntegration.apply_kde_style()` pour appliquer le style KDE
- Les icônes proviennent du thème système KDE
- La fenêtre s'intègre au gestionnaire de fenêtres KDE

### Déploiement

#### Via .desktop
Le fichier [debian/linux-hello-gui.desktop](debian/linux-hello-gui.desktop) permet:
- Lancer via le menu d'applications KDE
- Utiliser Ctrl+Espace pour rechercher l'app

#### Via PolicyKit
Le fichier [debian/com.linux-hello.gui.policy](debian/com.linux-hello.gui.policy) gère:
- Escalade sécurisée de privilèges (sudo)
- Authentification pour modifications système

## Modification des Widgets

### Ajouter un nouvel onglet

1. Créer une nouvelle classe `QWidget` dans `src/linux_hello_gui/new_feature.py`:

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class NewFeatureWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Nouvelle fonctionnalité"))
        self.setLayout(layout)
```

2. L'ajouter dans [window.py](src/linux_hello_gui/window.py):

```python
from .new_feature import NewFeatureWidget

# Dans __init__ de MainWindow:
self.new_widget = NewFeatureWidget()
self.tabs.addTab(self.new_widget, "📋 Nouvelle")
```

## Appels Système

L'application utilise `subprocess` pour:

1. **Lecture PAM** - lecture simple
2. **Écriture PAM** - utilise `sudo tee`
3. **Modification config** - essai direct, puis `sudo` en cas d'erreur

Exemple:
```python
result = subprocess.run(
    ['sudo', 'tee', '/etc/pam.d/linux-hello'],
    input=config_content,
    text=True,
    capture_output=True
)
```

## Débogage

### Activer les logs détaillés

```bash
PYTHONUNBUFFERED=1 linux-hello-gui
```

### Vérifier les permissions

```bash
ls -la /etc/linux-hello/
ls -la /etc/pam.d/linux-hello
ls -la /etc/linux-hello/config.json
```

### Test de caméra

```bash
python3 -c "
import cv2
cap = cv2.VideoCapture(0)
print('Camera available:', cap.isOpened())
cap.release()
"
```

## Contribution

1. Respecter PEP 8
2. Ajouter des docstrings
3. Tester avec `make test`
4. Formatter avec `make format`

## Ressources

- [PySide6 Documentation](https://doc.qt.io/qtforpython/)
- [OpenCV Python API](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [KDE Integration](https://develop.kde.org/)
- [PolicyKit Documentation](https://www.freedesktop.org/wiki/Software/polkit/)
