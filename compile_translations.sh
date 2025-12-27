#!/bin/bash
# Compile translation files

for lang in ar de en es it ja pt ru zh_CN; do
    po_file="po/${lang}.po"
    if [ -f "$po_file" ]; then
        # Ensure directory exists
        mkdir -p "src/linux_hello_gui/locale/${lang}/LC_MESSAGES"
        
        # Compile .po to .mo
        msgfmt -o "src/linux_hello_gui/locale/${lang}/LC_MESSAGES/linux-hello-gui.mo" "$po_file"
        echo "✓ Compiled: $lang"
    fi
done
