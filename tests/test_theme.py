"""Tests for the Wabi Sphinx Theme core functionality."""

from pathlib import Path

import wabi_sphinx_theme
from wabi_sphinx_theme import (
    WabiStyle,
    _parse_json_option,
    _update_context,
    get_html_theme_path,
    setup,
)


class TestThemePackage:
    """Test the theme package structure and imports."""

    def test_version_exists(self) -> None:
        """Test that version string is defined."""
        assert hasattr(wabi_sphinx_theme, "__version__")
        assert isinstance(wabi_sphinx_theme.__version__, str)
        assert wabi_sphinx_theme.__version__ == "0.1.0"

    def test_exports(self) -> None:
        """Test that all expected exports are available."""
        assert hasattr(wabi_sphinx_theme, "get_html_theme_path")
        assert hasattr(wabi_sphinx_theme, "setup")
        assert hasattr(wabi_sphinx_theme, "WabiStyle")

    def test_get_html_theme_path_returns_string(self) -> None:
        """Test that get_html_theme_path returns a string path."""
        path = get_html_theme_path()
        assert isinstance(path, str)

    def test_get_html_theme_path_exists(self) -> None:
        """Test that the theme path exists on disk."""
        path = Path(get_html_theme_path())
        assert path.exists()
        assert path.is_dir()


class TestThemeFiles:
    """Test that required theme files exist."""

    def test_theme_conf_exists(self, theme_path: Path) -> None:
        """Test that theme.conf exists."""
        theme_conf = theme_path / "theme.conf"
        assert theme_conf.exists(), "theme.conf is required for Sphinx themes"

    def test_css_exists(self, theme_path: Path) -> None:
        """Test that the main CSS file exists."""
        css_file = theme_path / "static" / "css" / "wabi.css"
        assert css_file.exists(), "wabi.css stylesheet is required"

    def test_layout_template_exists(self, theme_path: Path) -> None:
        """Test that the layout template exists."""
        layout = theme_path / "layout.html"
        assert layout.exists(), "layout.html template is required"

    def test_init_exists(self, theme_path: Path) -> None:
        """Test that __init__.py exists."""
        init_file = theme_path / "__init__.py"
        assert init_file.exists()

    def test_pygments_style_exists(self, theme_path: Path) -> None:
        """Test that pygments_style.py exists."""
        pygments_file = theme_path / "pygments_style.py"
        assert pygments_file.exists()


class TestThemeConf:
    """Test theme.conf configuration."""

    def test_theme_conf_content(self, theme_path: Path) -> None:
        """Test that theme.conf has required sections."""
        theme_conf = theme_path / "theme.conf"
        content = theme_conf.read_text()

        # Check required sections
        assert "[theme]" in content
        assert "inherit = basic" in content
        assert "stylesheet = css/wabi.css" in content

    def test_theme_conf_options(self, theme_path: Path) -> None:
        """Test that theme.conf has expected options."""
        theme_conf = theme_path / "theme.conf"
        content = theme_conf.read_text()

        assert "[options]" in content
        assert "site_title" in content
        assert "site_url" in content

    def test_theme_conf_has_nav_links(self, theme_path: Path) -> None:
        """Test that theme.conf has configurable nav_links."""
        theme_conf = theme_path / "theme.conf"
        content = theme_conf.read_text()

        assert "nav_links" in content
        assert "nav_show_docs_link" in content
        assert "nav_docs_label" in content

    def test_theme_conf_has_footer_links(self, theme_path: Path) -> None:
        """Test that theme.conf has configurable footer_links."""
        theme_conf = theme_path / "theme.conf"
        content = theme_conf.read_text()

        assert "footer_links" in content
        assert "footer_copyright" in content


class TestPygmentsStyle:
    """Test the custom Pygments style."""

    def test_wabi_style_exists(self) -> None:
        """Test that WabiStyle is importable."""
        assert WabiStyle is not None

    def test_wabi_style_has_name(self) -> None:
        """Test that WabiStyle has a name."""
        assert hasattr(WabiStyle, "name")
        assert WabiStyle.name == "wabi"

    def test_wabi_style_has_background_color(self) -> None:
        """Test that WabiStyle has correct background color."""
        assert hasattr(WabiStyle, "background_color")
        assert WabiStyle.background_color == "#2d2a26"

    def test_wabi_style_has_styles(self) -> None:
        """Test that WabiStyle defines token styles."""
        assert hasattr(WabiStyle, "styles")
        assert isinstance(WabiStyle.styles, dict)
        assert len(WabiStyle.styles) > 0


class TestCSSContent:
    """Test CSS file content."""

    def test_css_has_custom_properties(self, theme_path: Path) -> None:
        """Test that CSS defines expected custom properties."""
        css_file = theme_path / "static" / "css" / "wabi.css"
        content = css_file.read_text()

        # Check for Wabi color palette
        assert "--color-bg: #faf8f5" in content
        assert "--color-accent: #b8574c" in content
        assert "--color-text: #2d2a26" in content

    def test_css_has_typography(self, theme_path: Path) -> None:
        """Test that CSS defines typography variables."""
        css_file = theme_path / "static" / "css" / "wabi.css"
        content = css_file.read_text()

        assert "--font-display:" in content
        assert "--font-body:" in content
        assert "--font-mono:" in content
        assert "Fraunces" in content
        assert "Newsreader" in content

    def test_css_has_header_styles(self, theme_path: Path) -> None:
        """Test that CSS includes header navigation styles."""
        css_file = theme_path / "static" / "css" / "wabi.css"
        content = css_file.read_text()

        assert ".header" in content
        assert ".nav__link" in content
        assert ".footer" in content


class TestLayoutTemplate:
    """Test the layout template content."""

    def test_layout_extends_basic(self, theme_path: Path) -> None:
        """Test that layout extends basic theme."""
        layout = theme_path / "layout.html"
        content = layout.read_text()

        assert 'extends "basic/layout.html"' in content

    def test_layout_has_google_fonts(self, theme_path: Path) -> None:
        """Test that layout includes Google Fonts."""
        layout = theme_path / "layout.html"
        content = layout.read_text()

        assert "fonts.googleapis.com" in content
        assert "Fraunces" in content

    def test_layout_has_header(self, theme_path: Path) -> None:
        """Test that layout includes header block."""
        layout = theme_path / "layout.html"
        content = layout.read_text()

        assert "block header" in content
        assert 'class="header"' in content

    def test_layout_has_footer(self, theme_path: Path) -> None:
        """Test that layout includes footer block."""
        layout = theme_path / "layout.html"
        content = layout.read_text()

        assert "block footer" in content
        assert 'class="footer"' in content

    def test_layout_has_navigation(self, theme_path: Path) -> None:
        """Test that layout includes navigation links."""
        layout = theme_path / "layout.html"
        content = layout.read_text()

        assert 'class="nav"' in content
        assert "nav__link" in content

    def test_layout_supports_configurable_nav(self, theme_path: Path) -> None:
        """Test that layout uses configurable nav_links."""
        layout = theme_path / "layout.html"
        content = layout.read_text()

        # Check that template uses theme_nav_links (parsed by Python, not fromjson)
        assert "theme_nav_links" in content

    def test_layout_supports_configurable_footer(self, theme_path: Path) -> None:
        """Test that layout uses configurable footer_links."""
        layout = theme_path / "layout.html"
        content = layout.read_text()

        assert "theme_footer_links" in content


class TestSphinxSetup:
    """Test Sphinx extension setup."""

    def test_setup_returns_dict(self) -> None:
        """Test that setup returns extension metadata."""

        class MockApp:
            """Mock Sphinx application."""

            def add_html_theme(self, name: str, path: str) -> None:
                self.theme_name = name
                self.theme_path = path

            def connect(self, event: str, callback) -> None:
                """Mock event connection."""
                pass

        app = MockApp()
        result = setup(app)

        assert isinstance(result, dict)
        assert "version" in result
        assert "parallel_read_safe" in result
        assert "parallel_write_safe" in result

    def test_setup_registers_theme(self) -> None:
        """Test that setup registers the theme."""

        class MockApp:
            """Mock Sphinx application."""

            theme_name: str = ""
            theme_path: str = ""

            def add_html_theme(self, name: str, path: str) -> None:
                self.theme_name = name
                self.theme_path = path

            def connect(self, event: str, callback) -> None:
                """Mock event connection."""
                pass

        app = MockApp()
        setup(app)

        assert app.theme_name == "wabi_sphinx_theme"
        assert app.theme_path != ""


class TestJsonParsing:
    """Test JSON parsing helper functions."""

    def test_parse_json_option_empty_string(self) -> None:
        """Test parsing empty string returns empty list."""
        assert _parse_json_option("") == []

    def test_parse_json_option_none(self) -> None:
        """Test parsing None returns empty list."""
        assert _parse_json_option(None) == []

    def test_parse_json_option_valid_json(self) -> None:
        """Test parsing valid JSON string."""
        result = _parse_json_option('[{"name": "Test", "url": "/test/"}]')
        assert result == [{"name": "Test", "url": "/test/"}]

    def test_parse_json_option_list_passthrough(self) -> None:
        """Test that lists are passed through unchanged."""
        input_list = [{"name": "Test", "url": "/test/"}]
        assert _parse_json_option(input_list) == input_list

    def test_parse_json_option_invalid_json(self) -> None:
        """Test parsing invalid JSON returns empty list."""
        assert _parse_json_option("not valid json") == []

    def test_parse_json_option_non_list_json(self) -> None:
        """Test parsing JSON object (not list) returns empty list."""
        assert _parse_json_option('{"key": "value"}') == []

    def test_update_context_parses_nav_links(self) -> None:
        """Test that _update_context parses nav_links."""
        context = {
            "theme_nav_links": '[{"name": "Test", "url": "/test/"}]',
            "theme_footer_links": "",
        }
        _update_context(None, None, None, context, None)
        assert context["theme_nav_links"] == [{"name": "Test", "url": "/test/"}]
        assert context["theme_footer_links"] == []

    def test_update_context_parses_footer_links(self) -> None:
        """Test that _update_context parses footer_links."""
        context = {
            "theme_nav_links": "",
            "theme_footer_links": '[{"name": "GitHub", "url": "https://github.com"}]',
        }
        _update_context(None, None, None, context, None)
        assert context["theme_nav_links"] == []
        assert context["theme_footer_links"] == [{"name": "GitHub", "url": "https://github.com"}]
