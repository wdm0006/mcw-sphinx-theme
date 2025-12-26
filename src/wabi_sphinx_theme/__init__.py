"""
Wabi Sphinx Theme
=================

A warm, minimal Sphinx theme matching the Wabi Hugo theme.
Named after wabi-sabi - finding beauty in simplicity and imperfection.

Features:
- Cream, sand, and terracotta color palette
- Fraunces display font for headings
- Newsreader body font for reading
- Instrument Sans for UI elements
- IBM Plex Mono for code
- Matching navigation from mcginniscommawill.com
"""

from pathlib import Path

__version__ = "0.1.0"

# Export the Pygments style for easy access
from wabi_sphinx_theme.pygments_style import WabiStyle

__all__ = ["WabiStyle", "__version__", "get_html_theme_path", "setup"]


def get_html_theme_path():
    """Return the path to the theme templates."""
    return str(Path(__file__).parent)


def setup(app):
    """Sphinx extension setup function."""
    app.add_html_theme("wabi_sphinx_theme", get_html_theme_path())

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
