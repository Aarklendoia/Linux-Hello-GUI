.PHONY: help install install-dev run test clean build

help:
	@echo "Linux Hello GUI – Makefile"
	@echo ""
	@echo "Cibles disponibles:"
	@echo "  install       - Installer l'application"
	@echo "  install-dev   - Installer en mode développement"
	@echo "  run           - Lancer l'application"
	@echo "  test          - Exécuter les tests d'importation"
	@echo "  clean         - Nettoyer les fichiers de build"
	@echo "  build         - Construire le package"

install:
	pip install .

install-dev:
	pip install -e .
	pip install black flake8 pytest

run:
	python -m linux_hello_gui.main

test:
	python test_imports.py

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

lint:
	flake8 src/linux_hello_gui/ --max-line-length=100
	black src/linux_hello_gui/ --check

format:
	black src/linux_hello_gui/

.PHONY: help install install-dev run test clean build lint format
