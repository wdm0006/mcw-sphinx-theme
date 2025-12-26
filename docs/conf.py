"""
Sphinx configuration for Wabi Sphinx Theme documentation.
"""

import json
import sys
from pathlib import Path

# Add the theme to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Project information
project = "Wabi Sphinx Theme"
copyright = "2025, Will McGinnis"
author = "Will McGinnis"
release = "0.1.0"

# General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# HTML output options
html_theme = "wabi_sphinx_theme"

html_theme_options = {
    # Site branding
    "site_title": "McGinnis, Will",
    "site_url": "https://mcginniscommawill.com",
    # Navigation links - JSON array of {name, url} objects
    # These appear in the top nav before the "Docs" link
    "nav_links": json.dumps([
        {"name": "Guides", "url": "/guides/"},
        {"name": "Topics", "url": "/topics/"},
        {"name": "Blog", "url": "/posts/"},
        {"name": "About", "url": "/about/"},
        {"name": "Free Coffee", "url": "/coffee/"},
        {"name": "OSS", "url": "/oss/"},
    ]),
    # Show the "Docs" link in nav (points to documentation root)
    "nav_show_docs_link": True,
    "nav_docs_label": "Docs",
    # Footer links - JSON array of {name, url} objects
    "footer_links": json.dumps([
        {"name": "GitHub", "url": "https://github.com/wdm0006"},
        {"name": "LinkedIn", "url": "https://www.linkedin.com/in/wmcginnis/"},
        {"name": "Twitter", "url": "https://x.com/willmcginniser"},
    ]),
    # Breadcrumb options
    "show_breadcrumbs": True,
    "show_home_breadcrumb": True,
}

# Pygments style - use the Wabi style
pygments_style = "wabi_sphinx_theme.pygments_style.WabiStyle"
