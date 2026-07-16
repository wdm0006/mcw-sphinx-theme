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
import posixpath
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


def _update_context(app, pagename, _templatename, context, _doctree):
    """Update template context with parsed JSON options and the page's output URI."""
    theme_options = context.get("theme_nav_links", "")
    context["theme_nav_links"] = _parse_json_option(theme_options)

    theme_options = context.get("theme_footer_links", "")
    context["theme_footer_links"] = _parse_json_option(theme_options)

    builder = getattr(app, "builder", None)
    if builder is not None:
        # Builder-specific: ".html" for html, "page/" for dirhtml, honours html_file_suffix.
        page_uri = builder.get_target_uri(pagename)
        context["wabi_page_uri"] = page_uri

        # Sphinx < 8.0 builds pageurl as html_baseurl + pagename + out_suffix, which is
        # wrong for any builder whose output URI is not "<pagename>.html" (e.g. dirhtml).
        # Recompute it the way Sphinx 8 does so canonical/og:url agree on every version.
        if app.config.html_baseurl:
            context["pageurl"] = posixpath.join(app.config.html_baseurl, page_uri)


def setup(app):
    """Sphinx extension setup function."""
    app.add_html_theme("wabi_sphinx_theme", get_html_theme_path())
    app.connect("html-page-context", _update_context)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
