#!/usr/bin/env python3
"""Setup script for Linux Hello GUI."""

from setuptools import setup, find_packages
from pathlib import Path

# Read version from pyproject.toml
here = Path(__file__).resolve().parent
version = '1.0.0'

setup(
    name='linux-hello-gui',
    version=version,
    description='Interface graphique pour Linux-Hello',
    author='Édouard Biton',
    author_email='aarklendoia@proton.me',
    url='https://github.com/ebiton/Linux-Hello',
    license='GPL-3.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={
        'linux_hello_gui': [
            'locale/*/LC_MESSAGES/*.mo',
        ],
    },
    install_requires=[
        'PySide6>=6.4',
        'opencv-python>=4.8',
    ],
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'linux-hello-gui=linux_hello_gui.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
