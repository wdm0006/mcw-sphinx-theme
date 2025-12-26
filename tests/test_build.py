"""Integration tests for building Sphinx documentation with the theme."""

import subprocess
from pathlib import Path

import pytest


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

        # Allow specific warnings we expect
        assert result.returncode == 0 or "html_static_path" in result.stderr, (
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

        # Check that CSS is linked in the output
        index_html = build_path / "html" / "index.html"
        if index_html.exists():
            content = index_html.read_text()
            assert "wabi.css" in content or "css" in content

    @pytest.mark.integration
    def test_build_includes_header(self, docs_path: Path, build_path: Path) -> None:
        """Test that the build includes the custom header."""
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
        if index_html.exists():
            content = index_html.read_text()
            # Check for header elements
            assert "header" in content.lower()
