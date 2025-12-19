#!/usr/bin/env python3
"""Privilege escalation helper for Linux Hello GUI."""

import sys
import subprocess
import os


def check_sudo_password():
    """Check if user has sudo access."""
    result = subprocess.run(
        ['sudo', '-n', 'true'],
        capture_output=True,
        timeout=1
    )
    return result.returncode == 0


def run_with_sudo(command):
    """Run a command with sudo."""
    try:
        result = subprocess.run(
            ['sudo'] + command,
            capture_output=True,
            text=True
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)


def get_sudo_access():
    """Get sudo access for configuration operations."""
    print("Cette opération nécessite les droits administrateur.")
    print("Veuillez entrer votre mot de passe (sudo)...")
    
    result = subprocess.run(['sudo', '-v'])
    return result.returncode == 0


if __name__ == "__main__":
    if get_sudo_access():
        print("✓ Accès administrateur obtenu")
        sys.exit(0)
    else:
        print("✗ Accès administrateur refusé")
        sys.exit(1)
