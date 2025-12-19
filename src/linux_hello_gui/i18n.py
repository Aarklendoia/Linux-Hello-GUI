"""Internationalization (i18n) module for Linux Hello GUI."""

import os
import gettext
from pathlib import Path

# Supported languages
SUPPORTED_LANGUAGES = {
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

# Default language
DEFAULT_LANGUAGE = 'en'

# Translation catalogs directory
# Look in multiple locations: development (src/linux_hello_gui/locale)
# and installed system (/usr/share/linux-hello-gui/locale)
def _get_locale_dir():
    """Get locale directory path."""
    # First try development directory
    dev_locale = Path(__file__).parent / 'locale'
    if dev_locale.exists():
        return dev_locale
    
    # Then try system installation
    system_locale = Path('/usr/share/linux-hello-gui/locale')
    if system_locale.exists():
        return system_locale
    
    # Fallback to development
    return dev_locale

LOCALE_DIR = _get_locale_dir()


def setup_gettext(language=None):
    """Setup gettext translation.
    
    Args:
        language: Language code (e.g., 'en', 'fr'). If None, uses system locale.
    """
    global _translation
    
    if language is None:
        language = os.environ.get('LANGUAGE', DEFAULT_LANGUAGE).split(':')[0]
    
    # Normalize language code
    if language not in SUPPORTED_LANGUAGES:
        language = DEFAULT_LANGUAGE
    
    try:
        # Try to load translation catalog
        translation = gettext.translation(
            'linux-hello-gui',
            localedir=str(LOCALE_DIR),
            languages=[language],
            fallback=True
        )
        _translation = translation.gettext
    except Exception:
        _translation = lambda x: x


def get_available_languages():
    """Get list of available languages."""
    return SUPPORTED_LANGUAGES


def get_language_name(lang_code):
    """Get display name for language code."""
    return SUPPORTED_LANGUAGES.get(lang_code, lang_code)


def set_language(language):
    """Set active language and reload translations."""
    setup_gettext(language)


def _(message):
    """Translate message."""
    return _translation(message)


def ngettext(singular, plural, count):
    """Translate plural forms."""
    try:
        return _translation.ngettext(singular, plural, count)
    except (AttributeError, TypeError):
        return singular if count == 1 else plural


# Initialize with default language
_translation = lambda x: x
setup_gettext()
