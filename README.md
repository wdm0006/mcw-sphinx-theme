# Wabi Sphinx Theme

A warm, minimal Sphinx theme matching the [Wabi Hugo theme](https://mcginniscommawill.com). Named after *wabi-sabi* - finding beauty in simplicity and imperfection.

This theme is designed to match the look and feel of mcginniscommawill.com by default, but is fully configurable for use with any project.

## Features

- **Warm Color Palette**: Cream, sand, and terracotta tones
- **Typography**: Fraunces (headings), Newsreader (body), Instrument Sans (UI), IBM Plex Mono (code)
- **Configurable Navigation**: Customize header and footer links via JSON config
- **Responsive**: Mobile-friendly with collapsible navigation
- **Custom Pygments Style**: Warm syntax highlighting that matches the theme

## Installation

```bash
pip install wabi-sphinx-theme
```

Or with uv:

```bash
uv add wabi-sphinx-theme
```

## Quick Start

In your `conf.py`:

```python
html_theme = "wabi_sphinx_theme"
```

That's it! The theme works with sensible defaults.

## Configuration

### Standalone Documentation

For standalone docs (not part of a larger site):

```python
import json

html_theme = "wabi_sphinx_theme"

html_theme_options = {
    "site_title": "My Project",
    "site_url": "",  # Empty for standalone

    # Just show docs link in nav
    "nav_links": "[]",
    "nav_show_docs_link": True,
    "nav_docs_label": "Documentation",

    # Footer links
    "footer_links": json.dumps([
        {"name": "GitHub", "url": "https://github.com/user/project"},
    ]),
}
```

### Integrated with Main Site

For docs that are part of a larger website:

```python
import json

html_theme = "wabi_sphinx_theme"

html_theme_options = {
    "site_title": "My Site",
    "site_url": "https://example.com",

    # Navigation matching your main site
    "nav_links": json.dumps([
        {"name": "Blog", "url": "/blog/"},
        {"name": "About", "url": "/about/"},
        {"name": "GitHub", "url": "https://github.com/user", "external": True},
    ]),
    "nav_show_docs_link": True,
    "nav_docs_label": "Docs",

    # Footer
    "footer_links": json.dumps([
        {"name": "GitHub", "url": "https://github.com/user"},
        {"name": "Twitter", "url": "https://twitter.com/user"},
    ]),

    # Breadcrumbs
    "show_breadcrumbs": True,
    "show_home_breadcrumb": True,
}
```

### All Options

| Option | Default | Description |
|--------|---------|-------------|
| `site_title` | "McGinnis, Will" | Header title |
| `site_url` | "https://mcginniscommawill.com" | Base URL for nav links |
| `nav_links` | (see defaults) | JSON array of `{name, url}` objects |
| `nav_show_docs_link` | `True` | Show "Docs" link in nav |
| `nav_docs_label` | "Docs" | Label for docs link |
| `footer_links` | (see defaults) | JSON array of footer links |
| `footer_copyright` | "" | Custom copyright text |
| `show_breadcrumbs` | `True` | Show breadcrumb navigation |
| `show_home_breadcrumb` | `True` | Include "Home" in breadcrumbs |

## Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Background | `#faf8f5` | Main background |
| Background Subtle | `#f5f2ed` | Sidebar, cards |
| Background Accent | `#ebe6de` | Inline code, hover |
| Text | `#2d2a26` | Primary text |
| Text Muted | `#6b6560` | Secondary text |
| Text Subtle | `#9a948d` | Tertiary text |
| Accent | `#b8574c` | Links, highlights |
| Accent Hover | `#a04a40` | Link hover |
| Accent Subtle | `#d4a59e` | Decorative |

## Typography

- **Fraunces**: Quirky soft serif with optical sizing - headlines
- **Newsreader**: Elegant editorial serif - body text
- **Instrument Sans**: Warm humanist sans - UI elements
- **IBM Plex Mono**: Clean monospace - code

## Syntax Highlighting

Use the included Pygments style:

```python
pygments_style = "wabi_sphinx_theme.pygments_style.WabiStyle"
```

## Development

```bash
# Clone and install
git clone https://github.com/wdm0006/wabi-sphinx-theme.git
cd wabi-sphinx-theme
uv sync --all-extras

# Run tests
make test

# Build docs
make docs

# Format and lint
make format
make lint
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Credits

- Design inspired by Scandinavian and Japanese aesthetics
- Typography selection based on the Wabi Hugo theme
- Named after wabi-sabi (侘寂) - the Japanese philosophy of finding beauty in imperfection
