"""Integration tests for building Sphinx documentation with the theme."""

import re
import subprocess
from pathlib import Path

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
