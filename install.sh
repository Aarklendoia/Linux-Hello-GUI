#!/bin/bash
# Installation script for Linux Hello GUI

set -e

echo "=== Installation de Linux Hello GUI ==="
echo ""

# Check Python version
python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
required_version="3.9"

if (( $(echo "$python_version < $required_version" | bc -l) )); then
    echo "✗ Python $required_version.x ou supérieur requis (actuellement: $python_version)"
    exit 1
fi

echo "✓ Python $python_version détecté"
echo ""

# Install dependencies
echo "Installation des dépendances Python..."
pip install --upgrade pip setuptools wheel
pip install PySide6 opencv-python

echo "✓ Dépendances installées"
echo ""

# Install the package
echo "Installation de linux-hello-gui..."
pip install -e .

echo "✓ Installation complète"
echo ""

# Check if GUI can be launched
echo "Vérification de l'installation..."
python3 test_imports.py

echo ""
echo "=== Installation réussie ==="
echo ""
echo "Utilisez 'linux-hello-gui' pour lancer l'application"
