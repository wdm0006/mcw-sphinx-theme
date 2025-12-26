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

import json
from pathlib import Path

__version__ = "0.1.0"

# Export the Pygments style for easy access
from wabi_sphinx_theme.pygments_style import WabiStyle

__all__ = ["WabiStyle", "__version__", "get_html_theme_path", "setup"]


def get_html_theme_path():
    """Return the path to the theme templates."""
    return str(Path(__file__).parent)


def _parse_json_option(value):
    """Parse a JSON string option, returning empty list if invalid."""
    if not value:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, list) else []
        except (json.JSONDecodeError, TypeError):
            return []
    return []


def _update_context(_app, _pagename, _templatename, context, _doctree):
    """Update template context with parsed JSON options."""
    theme_options = context.get("theme_nav_links", "")
    context["theme_nav_links"] = _parse_json_option(theme_options)

    theme_options = context.get("theme_footer_links", "")
    context["theme_footer_links"] = _parse_json_option(theme_options)


def setup(app):
    """Sphinx extension setup function."""
    app.add_html_theme("wabi_sphinx_theme", get_html_theme_path())
    app.connect("html-page-context", _update_context)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
