#!/usr/bin/env python3
"""Extract translatable strings and create .po files."""

import os
import re
from pathlib import Path

# Supported languages
LANGUAGES = {
    'ar': 'العربية',
    'de': 'Deutsch',
    'en': 'English',
    'es': 'Español',
    'fr': 'Français',
    'it': 'Italiano',
    'ja': '日本語',
    'pt': 'Português',
    'ru': 'Русский',
    'zh_CN': '简体中文',
}

PO_TEMPLATE = """# {lang_name} translation for Linux Hello GUI
# Copyright (C) 2025 Linux Hello Contributors
#
msgid ""
msgstr ""
"Project-Id-Version: linux-hello-gui 1.0.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Language: {lang_code}\\n"

msgid "Linux Hello – Configuration"
msgstr ""

msgid "Ready"
msgstr ""

msgid "&File"
msgstr ""

msgid "&Settings"
msgstr ""

msgid "&Quit"
msgstr ""

msgid "&Language"
msgstr ""

msgid "&Help"
msgstr ""

msgid "&About"
msgstr ""

msgid "About &Qt"
msgstr ""

msgid "Language Changed"
msgstr ""

msgid "Please restart the application for language changes to take effect."
msgstr ""

msgid "Settings"
msgstr ""

msgid "Settings can be modified in the Settings tab."
msgstr ""

msgid "About Linux Hello"
msgstr ""

msgid "Linux Hello – Configuration\\nVersion 1.0.0\\n\\nGraphical interface to configure the Linux Hello facial recognition service.\\n\\n© Linux Hello Contributors"
msgstr ""

msgid "Face Enrollment"
msgstr ""

msgid "Camera:"
msgstr ""

msgid "Refresh"
msgstr ""

msgid "Press 'Start Camera' to see preview"
msgstr ""

msgid "Username:"
msgstr ""

msgid "Ex: john.doe"
msgstr ""

msgid "Number of photos:"
msgstr ""

msgid "Start Camera"
msgstr ""

msgid "Stop Camera"
msgstr ""

msgid "Enroll Face"
msgstr ""

msgid "Error"
msgstr ""

msgid "Cannot open camera"
msgstr ""

msgid "Camera stopped"
msgstr ""

msgid "Please enter a username"
msgstr ""

msgid "Camera is not active"
msgstr ""

msgid "Success"
msgstr ""

msgid "Face for {{username}} enrolled with {{count}} photos"
msgstr ""

msgid "Incomplete enrollment: {{captured}}/{{total}} photos captured"
msgstr ""

msgid "PAM Configuration (Authentication)"
msgstr ""

msgid "PAM (Pluggable Authentication Modules) allows using facial recognition for system authentication."
msgstr ""

msgid "PAM Configuration"
msgstr ""

msgid "Preset configuration:"
msgstr ""

msgid "Strict (facial recognition required)"
msgstr ""

msgid "Medium (facial recognition + password)"
msgstr ""

msgid "Permissive (facial recognition optional)"
msgstr ""

msgid "Apply"
msgstr ""

msgid "Options"
msgstr ""

msgid "Facial recognition required"
msgstr ""

msgid "Allow password as fallback"
msgstr ""

msgid "Cache results"
msgstr ""

msgid "Save Configuration"
msgstr ""

msgid "Reload from Disk"
msgstr ""

msgid "# PAM configuration not found"
msgstr ""

msgid "Error: Permission denied to read PAM configuration"
msgstr ""

msgid "Error: {{error}}"
msgstr ""

msgid "Confirmation"
msgstr ""

msgid "Are you sure you want to modify the PAM configuration?\\nThis requires administrator privileges."
msgstr ""

msgid "PAM configuration saved successfully"
msgstr ""

msgid "Error saving configuration: {{error}}"
msgstr ""

msgid "Linux Hello Settings"
msgstr ""

msgid "Camera Settings"
msgstr ""

msgid "Default camera index:"
msgstr ""

msgid "Video width:"
msgstr ""

msgid "Video height:"
msgstr ""

msgid "Recognition Settings"
msgstr ""

msgid "Similarity threshold:"
msgstr ""

msgid "Minimum confidence:"
msgstr ""

msgid "Performance Settings"
msgstr ""

msgid "Timeout:"
msgstr ""

msgid "Max frames:"
msgstr ""

msgid " seconds"
msgstr ""

msgid "Logging"
msgstr ""

msgid "Log level:"
msgstr ""

msgid "Enable logging"
msgstr ""

msgid "Save"
msgstr ""

msgid "Reload"
msgstr ""

msgid "Reset to Defaults"
msgstr ""

msgid "Error loading configuration: {{error}}"
msgstr ""

msgid "Are you sure you want to save this configuration?\\nThis may require administrator privileges."
msgstr ""

msgid "Configuration saved successfully"
msgstr ""

msgid "Error saving configuration: {{error}}"
msgstr ""

msgid "Are you sure you want to reset to default settings?"
msgstr ""

msgid "👤 Face"
msgstr ""

msgid "🔐 PAM"
msgstr ""

msgid "⚙️ Settings"
msgstr ""
"""

def create_po_files():
    """Create .po files for all languages."""
    po_dir = Path(__file__).parent
    
    for lang_code, lang_name in LANGUAGES.items():
        # Skip if already exists (except en)
        po_file = po_dir / f"{lang_code}.po"
        if po_file.exists() and lang_code != 'en':
            print(f"Skipping {lang_code}: file already exists")
            continue
        
        content = PO_TEMPLATE.format(lang_code=lang_code, lang_name=lang_name)
        po_file.write_text(content, encoding='utf-8')
        print(f"Created: {po_file}")

if __name__ == '__main__':
    create_po_files()
    print("Done!")
