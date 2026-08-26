"""Integration tests for the SEO meta tags rendered by the theme's layout."""

import re
import subprocess
from pathlib import Path

import pytest

DESCRIPTION_RE = re.compile(r'<meta name="description" content="([^"]*)"')
OG_TITLE_RE = re.compile(r'<meta property="og:title" content="([^"]*)"')
OG_DESCRIPTION_RE = re.compile(r'<meta property="og:description" content="([^"]*)"')
OG_TYPE_RE = re.compile(r'<meta property="og:type" content="([^"]*)"')
OG_URL_RE = re.compile(r'<meta property="og:url" content="([^"]*)"')
OG_IMAGE_RE = re.compile(r'<meta property="og:image" content="([^"]*)"')
OG_SITE_NAME_RE = re.compile(r'<meta property="og:site_name" content="([^"]*)"')
TWITTER_CARD_RE = re.compile(r'<meta name="twitter:card" content="([^"]*)"')
TWITTER_TITLE_RE = re.compile(r'<meta name="twitter:title" content="([^"]*)"')
TWITTER_SITE_RE = re.compile(r'<meta name="twitter:site" content="([^"]*)"')
TWITTER_IMAGE_RE = re.compile(r'<meta name="twitter:image" content="([^"]*)"')
CANONICAL_RE = re.compile(r'<link rel="canonical" href="([^"]*)"')

PROJECT = "SEO Test"


def _write_project(src: Path, theme_options: dict) -> None:
    """Write a minimal Sphinx project using the theme with the given options."""
    src.mkdir(parents=True, exist_ok=True)
    (src / "conf.py").write_text(
        f"project = {PROJECT!r}\n"
        'html_theme = "wabi_sphinx_theme"\n'
        f"html_theme_options = {theme_options!r}\n"
    )
    (src / "index.rst").write_text("Index\n=====\n\n.. toctree::\n\n   page\n")
    (src / "page.rst").write_text("Page\n====\n\nBody text.\n")


def _build_page(tmp_path: Path, theme_options: dict) -> str:
    """Build a project with the given theme options and return page.html's contents."""
    src, out = tmp_path / "src", tmp_path / "out"
    _write_project(src, theme_options)
    result = subprocess.run(
        ["sphinx-build", "-b", "html", "-W", str(src), str(out)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        f"Sphinx build failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )
    page_html = out / "page.html"
    assert page_html.exists(), "Build should create page.html"
    return page_html.read_text()


class TestExampleDocsSeoTags:
    """The theme's own docs exercise the default configuration end to end."""

    @pytest.mark.integration
    def test_index_emits_the_full_seo_tag_set(self, docs_path: Path, build_path: Path) -> None:
        """The default config emits description, Open Graph, Twitter Card and canonical tags."""
        out = build_path / "html"
        result = subprocess.run(
            ["sphinx-build", "-b", "html", "-W", str(docs_path), str(out)],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, (
            f"Sphinx build failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )
        index_html = out / "index.html"
        assert index_html.exists(), "Build should create index.html"
        content = index_html.read_text()

        # docs/conf.py sets project and leaves site_url at the theme default.
        project = "Wabi Sphinx Theme"
        site_url = "https://mcginniscommawill.com"

        og_titles = OG_TITLE_RE.findall(content)
        assert len(og_titles) == 1 and og_titles[0], "Exactly one non-empty og:title expected"
        page_title = og_titles[0]
        expected_description = f"{page_title} - {project} documentation"

        assert DESCRIPTION_RE.findall(content) == [expected_description]
        assert OG_DESCRIPTION_RE.findall(content) == [expected_description]
        assert OG_TYPE_RE.findall(content) == ["website"]
        assert OG_SITE_NAME_RE.findall(content) == [project]
        assert TWITTER_CARD_RE.findall(content) == ["summary_large_image"]
        assert TWITTER_TITLE_RE.findall(content) == [page_title]

        # No html_baseurl and no docs_base_url, so the URLs come from site_url.
        assert OG_URL_RE.findall(content) == [f"{site_url}/index.html"]
        assert CANONICAL_RE.findall(content) == [f"{site_url}/index.html"]


class TestOptionalSeoTags:
    """og:image, twitter:image and twitter:site are conditional on theme options."""

    @pytest.mark.integration
    def test_image_and_site_tags_present_when_configured(self, tmp_path: Path) -> None:
        """og_image and twitter_site produce their tags verbatim."""
        content = _build_page(
            tmp_path,
            {
                "docs_base_url": "https://example.com/docs/",
                "og_image": "https://example.com/card.png",
                "twitter_site": "@example",
            },
        )

        assert OG_IMAGE_RE.findall(content) == ["https://example.com/card.png"]
        assert TWITTER_IMAGE_RE.findall(content) == ["https://example.com/card.png"]
        assert TWITTER_SITE_RE.findall(content) == ["@example"]

    @pytest.mark.integration
    def test_image_and_site_tags_absent_when_unset(self, tmp_path: Path) -> None:
        """Leaving og_image and twitter_site unset emits no image or site tags at all."""
        content = _build_page(tmp_path, {"docs_base_url": "https://example.com/docs/"})

        assert OG_IMAGE_RE.findall(content) == []
        assert TWITTER_IMAGE_RE.findall(content) == []
        assert TWITTER_SITE_RE.findall(content) == []
        # The unconditional tags still render, so absence is not a broken build.
        assert TWITTER_CARD_RE.findall(content) == ["summary_large_image"]

    @pytest.mark.integration
    def test_og_image_alone_still_emits_twitter_image(self, tmp_path: Path) -> None:
        """twitter:image is driven by og_image, not by twitter_site."""
        content = _build_page(
            tmp_path,
            {
                "docs_base_url": "https://example.com/docs/",
                "og_image": "https://example.com/card.png",
            },
        )

        assert OG_IMAGE_RE.findall(content) == ["https://example.com/card.png"]
        assert TWITTER_IMAGE_RE.findall(content) == ["https://example.com/card.png"]
        assert TWITTER_SITE_RE.findall(content) == []


class TestSeoBaseUrl:
    """seo_base_url prefers docs_base_url and falls back to site_url."""

    @pytest.mark.integration
    def test_docs_base_url_wins_over_site_url(self, tmp_path: Path) -> None:
        """With both set, canonical and og:url are built from docs_base_url."""
        content = _build_page(
            tmp_path,
            {
                "site_url": "https://main.example.com",
                "docs_base_url": "https://docs.example.com/",
            },
        )

        assert CANONICAL_RE.findall(content) == ["https://docs.example.com/page.html"]
        assert OG_URL_RE.findall(content) == ["https://docs.example.com/page.html"]

    @pytest.mark.integration
    def test_site_url_used_when_docs_base_url_unset(self, tmp_path: Path) -> None:
        """Without docs_base_url the URLs fall back to site_url."""
        content = _build_page(tmp_path, {"site_url": "https://main.example.com"})

        assert CANONICAL_RE.findall(content) == ["https://main.example.com/page.html"]
        assert OG_URL_RE.findall(content) == ["https://main.example.com/page.html"]

    @pytest.mark.integration
    def test_no_url_tags_without_a_base_url(self, tmp_path: Path) -> None:
        """An empty site_url and no docs_base_url means no canonical and no og:url."""
        content = _build_page(tmp_path, {"site_url": ""})

        assert CANONICAL_RE.findall(content) == []
        assert OG_URL_RE.findall(content) == []
        # The rest of the SEO block is unaffected.
        assert OG_TITLE_RE.findall(content) == ["Page"]
        assert TWITTER_CARD_RE.findall(content) == ["summary_large_image"]
