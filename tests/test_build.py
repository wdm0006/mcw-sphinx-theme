"""Integration tests for building Sphinx documentation with the theme."""

import re
import subprocess
from pathlib import Path
from typing import ClassVar

import pytest

CANONICAL_RE = re.compile(r'<link rel="canonical" href="([^"]*)"')
OG_URL_RE = re.compile(r'<meta property="og:url" content="([^"]*)"')


class TestSphinxBuild:
    """Test that Sphinx can build documentation with this theme."""

    @pytest.mark.integration
    def test_docs_build_succeeds(self, docs_path: Path, build_path: Path) -> None:
        """Test that the example docs build successfully."""
        result = subprocess.run(
            [
                "sphinx-build",
                "-b",
                "html",
                "-W",  # Treat warnings as errors
                str(docs_path),
                str(build_path / "html"),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, (
            f"Sphinx build failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )

    @pytest.mark.integration
    def test_build_creates_index(self, docs_path: Path, build_path: Path) -> None:
        """Test that the build creates an index.html."""
        subprocess.run(
            [
                "sphinx-build",
                "-b",
                "html",
                str(docs_path),
                str(build_path / "html"),
            ],
            capture_output=True,
            check=False,
        )

        index_html = build_path / "html" / "index.html"
        assert index_html.exists(), "Build should create index.html"

    @pytest.mark.integration
    def test_build_includes_css(self, docs_path: Path, build_path: Path) -> None:
        """Test that the build includes the theme CSS."""
        result = subprocess.run(
            [
                "sphinx-build",
                "-b",
                "html",
                str(docs_path),
                str(build_path / "html"),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, (
            f"Sphinx build failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )
        index_html = build_path / "html" / "index.html"
        assert index_html.exists(), "Build should create index.html"

        # Check that CSS is linked in the output
        content = index_html.read_text()
        assert "wabi.css" in content or "css" in content

    @pytest.mark.integration
    def test_build_includes_header(self, docs_path: Path, build_path: Path) -> None:
        """Test that the build includes the custom header."""
        result = subprocess.run(
            [
                "sphinx-build",
                "-b",
                "html",
                str(docs_path),
                str(build_path / "html"),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, (
            f"Sphinx build failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )
        index_html = build_path / "html" / "index.html"
        assert index_html.exists(), "Build should create index.html"

        content = index_html.read_text()
        # Check for header elements
        assert "header" in content.lower()


def _write_project(src: Path, *, extra_conf: str = "") -> None:
    """Write a minimal Sphinx project using the theme."""
    src.mkdir(parents=True, exist_ok=True)
    (src / "conf.py").write_text(
        'project = "SEO Test"\n'
        'html_theme = "wabi_sphinx_theme"\n'
        'html_theme_options = {"docs_base_url": "https://example.com/docs/"}\n' + extra_conf
    )
    (src / "index.rst").write_text("Index\n=====\n\n.. toctree::\n\n   page\n")
    (src / "page.rst").write_text("Page\n====\n\nBody text.\n")


def _build(src: Path, out: Path, builder: str) -> None:
    result = subprocess.run(
        ["sphinx-build", "-b", builder, "-W", str(src), str(out)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        f"Sphinx build failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )


class TestSeoUrls:
    """Test the rendered canonical and og:url tags from a real build."""

    @pytest.mark.integration
    def test_html_fallback_uses_docs_base_url(self, tmp_path: Path) -> None:
        """Without html_baseurl, URLs come from docs_base_url plus the .html suffix."""
        src, out = tmp_path / "src", tmp_path / "out"
        _write_project(src)
        _build(src, out, "html")

        content = (out / "page.html").read_text()
        assert CANONICAL_RE.findall(content) == ["https://example.com/docs/page.html"]
        assert OG_URL_RE.findall(content) == ["https://example.com/docs/page.html"]

    @pytest.mark.integration
    def test_dirhtml_urls_point_at_directory(self, tmp_path: Path) -> None:
        """Under dirhtml the page is served at /page/, so URLs must not end in .html."""
        src, out = tmp_path / "src", tmp_path / "out"
        _write_project(src)
        _build(src, out, "dirhtml")

        content = (out / "page" / "index.html").read_text()
        assert CANONICAL_RE.findall(content) == ["https://example.com/docs/page/"]
        assert OG_URL_RE.findall(content) == ["https://example.com/docs/page/"]

    @pytest.mark.integration
    def test_custom_file_suffix_is_honoured(self, tmp_path: Path) -> None:
        """A non-default html_file_suffix is reflected in the generated URLs."""
        src, out = tmp_path / "src", tmp_path / "out"
        _write_project(src, extra_conf='html_file_suffix = ".htm"\n')
        _build(src, out, "html")

        content = (out / "page.htm").read_text()
        assert CANONICAL_RE.findall(content) == ["https://example.com/docs/page.htm"]
        assert OG_URL_RE.findall(content) == ["https://example.com/docs/page.htm"]

    @pytest.mark.integration
    def test_html_baseurl_yields_single_canonical(self, tmp_path: Path) -> None:
        """With html_baseurl set, only Sphinx's own pageurl-based canonical is emitted."""
        src, out = tmp_path / "src", tmp_path / "out"
        _write_project(src, extra_conf='html_baseurl = "https://docs.example.org/"\n')
        _build(src, out, "html")

        content = (out / "page.html").read_text()
        assert CANONICAL_RE.findall(content) == ["https://docs.example.org/page.html"]
        assert OG_URL_RE.findall(content) == ["https://docs.example.org/page.html"]

    @pytest.mark.integration
    def test_html_baseurl_under_dirhtml(self, tmp_path: Path) -> None:
        """html_baseurl and dirhtml agree on a single directory-style canonical."""
        src, out = tmp_path / "src", tmp_path / "out"
        _write_project(src, extra_conf='html_baseurl = "https://docs.example.org/"\n')
        _build(src, out, "dirhtml")

        content = (out / "page" / "index.html").read_text()
        assert CANONICAL_RE.findall(content) == ["https://docs.example.org/page/"]
        assert OG_URL_RE.findall(content) == ["https://docs.example.org/page/"]


def _build_with_options(tmp_path: Path, options: str) -> subprocess.CompletedProcess:
    src, out = tmp_path / "src", tmp_path / "out"
    _write_project(src, extra_conf=f"html_theme_options.update({options})\n")
    return subprocess.run(
        ["sphinx-build", "-b", "html", "-W", str(src), str(out)],
        capture_output=True,
        text=True,
        check=False,
    )


class TestBooleanThemeOptions:
    """String and bool spellings of the boolean options render identically."""

    CASES: ClassVar[list[tuple[str, str]]] = [
        ("show_breadcrumbs", 'class="breadcrumbs"'),
        ("nav_show_docs_link", "nav__link--active"),
        ("show_home_breadcrumb", ">Home</a>"),
    ]

    @pytest.mark.integration
    @pytest.mark.parametrize(("option", "marker"), CASES)
    @pytest.mark.parametrize(
        ("value", "present"),
        [('"false"', False), ('"true"', True), ("True", True), ("False", False)],
    )
    def test_spellings(
        self, tmp_path: Path, option: str, marker: str, value: str, present: bool
    ) -> None:
        result = _build_with_options(tmp_path, f'{{"{option}": {value}}}')
        assert result.returncode == 0, result.stderr
        content = (tmp_path / "out" / "page.html").read_text()
        assert (marker in content) is present

    @pytest.mark.integration
    def test_garbage_value_fails_build(self, tmp_path: Path) -> None:
        result = _build_with_options(tmp_path, '{"show_breadcrumbs": "maybe"}')
        assert result.returncode != 0
        assert "show_breadcrumbs" in result.stderr
        assert "maybe" in result.stderr


class TestHtmlEscaping:
    """Interpolated values are escaped in text nodes and attributes (Sphinx does not autoescape)."""

    TITLE = "Tips & Tricks <beta>"
    ESCAPED_TITLE = "Tips &amp; Tricks &lt;beta&gt;"
    NASTY = 'Will "Bill" <McG> & Co'
    ESCAPED_NASTY = "Will &#34;Bill&#34; &lt;McG&gt; &amp; Co"

    def _build_nasty(self, tmp_path: Path) -> Path:
        src, out = tmp_path / "src", tmp_path / "out"
        nasty_opts = {
            "site_title": self.NASTY,
            "nav_docs_label": self.NASTY,
            "nav_links": [{"name": self.NASTY, "url": 'https://a.test/?q="x"&y=<z>'}],
            "footer_links": [{"name": self.NASTY, "url": 'https://b.test/?q="x"&y=<z>'}],
        }
        _write_project(
            src,
            extra_conf=(
                f"project = 'The \"Quoted\" Project'\nhtml_theme_options.update({nasty_opts!r})\n"
            ),
        )
        title = self.TITLE
        (src / "page.rst").write_text(f"{title}\n{'=' * len(title)}\n\n.. toctree::\n\n   child\n")
        (src / "child.rst").write_text("Child\n=====\n\nBody.\n")
        _build(src, out, "html")
        return out

    @pytest.mark.integration
    def test_breadcrumb_titles_escaped(self, tmp_path: Path) -> None:
        out = self._build_nasty(tmp_path)

        page = (out / "page.html").read_text()
        assert f"<span>{self.ESCAPED_TITLE}</span>" in page
        assert "<beta>" not in page

        child = (out / "child.html").read_text()
        assert f">{self.ESCAPED_TITLE}</a>" in child
        assert "<beta>" not in child

    @pytest.mark.integration
    def test_project_escaped_in_meta_attributes(self, tmp_path: Path) -> None:
        out = self._build_nasty(tmp_path)
        content = (out / "page.html").read_text()

        quoted = "The &#34;Quoted&#34; Project"
        assert re.findall(r'<meta name="description" content="([^"]*)"', content) == [
            f"{self.ESCAPED_TITLE} - {quoted} documentation"
        ]
        assert re.findall(r'<meta property="og:description" content="([^"]*)"', content) == [
            f"{self.ESCAPED_TITLE} - {quoted} documentation"
        ]
        assert re.findall(r'<meta name="twitter:description" content="([^"]*)"', content) == [
            f"{self.ESCAPED_TITLE} - {quoted} documentation"
        ]
        assert re.findall(r'<meta property="og:site_name" content="([^"]*)"', content) == [quoted]

    @pytest.mark.integration
    def test_theme_option_text_and_hrefs_escaped(self, tmp_path: Path) -> None:
        out = self._build_nasty(tmp_path)
        content = (out / "page.html").read_text()

        assert content.count(self.ESCAPED_NASTY) >= 5
        assert "<McG>" not in content
        escaped_query = "?q=&#34;x&#34;&amp;y=&lt;z&gt;"
        assert f'href="https://a.test/{escaped_query}"' in content
        assert f'href="https://b.test/{escaped_query}"' in content

    @pytest.mark.integration
    def test_copyright_stays_raw(self, tmp_path: Path) -> None:
        src, out = tmp_path / "src", tmp_path / "out"
        _write_project(
            src,
            extra_conf=(
                "html_theme_options.update({'footer_copyright': '<a href=\"/c\">Me</a> &amp; you'})\n"
            ),
        )
        _build(src, out, "html")
        assert '<a href="/c">Me</a> &amp; you' in (out / "page.html").read_text()
