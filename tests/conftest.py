"""Pytest configuration and fixtures for Wabi Sphinx Theme tests."""

from pathlib import Path

import pytest


@pytest.fixture
def theme_path() -> Path:
    """Return the path to the theme package."""
    return Path(__file__).parent.parent / "src" / "wabi_sphinx_theme"


@pytest.fixture
def docs_path() -> Path:
    """Return the path to the example docs."""
    return Path(__file__).parent.parent / "docs"


@pytest.fixture
def build_path(tmp_path: Path) -> Path:
    """Return a temporary path for build output."""
    build_dir = tmp_path / "_build"
    build_dir.mkdir(parents=True, exist_ok=True)
    return build_dir
