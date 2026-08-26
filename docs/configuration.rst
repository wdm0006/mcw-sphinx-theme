Configuration
=============

Basic Configuration
-------------------

To use the Wabi Sphinx Theme, add the following to your ``conf.py``::

    html_theme = "wabi_sphinx_theme"

Theme Options
-------------

The theme supports several configuration options via ``html_theme_options``.
All options have sensible defaults, so you only need to configure what you want to change.

Site Configuration
~~~~~~~~~~~~~~~~~~

Configure your site's branding and base URL:

.. code-block:: python

    html_theme_options = {
        # Site title shown in the header
        "site_title": "My Project",

        # Base URL for your main site (used for nav links)
        # Leave empty if docs are standalone
        "site_url": "https://example.com",
    }

Navigation Links
~~~~~~~~~~~~~~~~

Navigation links are fully configurable using a JSON array. Each link has:

- ``name`` (required): Display text
- ``url`` (required): Link URL (relative to site_url, or absolute)
- ``external`` (optional): Force external link behavior (auto-detected for http:// URLs)

.. code-block:: python

    import json

    html_theme_options = {
        # Custom navigation links
        "nav_links": json.dumps([
            {"name": "Blog", "url": "/blog/"},
            {"name": "About", "url": "/about/"},
            {"name": "GitHub", "url": "https://github.com/user/repo", "external": True},
        ]),

        # Show/hide the "Docs" link (points to documentation root)
        "nav_show_docs_link": True,

        # Customize the docs link label
        "nav_docs_label": "Docs",
    }

To disable all external nav links, set ``nav_links`` to an empty array:

.. code-block:: python

    html_theme_options = {
        "nav_links": "[]",  # No external nav links
    }

Footer Links
~~~~~~~~~~~~

Footer links work the same way as nav links:

.. code-block:: python

    import json

    html_theme_options = {
        "footer_links": json.dumps([
            {"name": "GitHub", "url": "https://github.com/user"},
            {"name": "Twitter", "url": "https://twitter.com/user"},
        ]),

        # Custom copyright (leave empty to use Sphinx's copyright)
        "footer_copyright": "© 2025 My Company",
    }

Breadcrumb Options
~~~~~~~~~~~~~~~~~~

Configure the breadcrumb navigation:

.. code-block:: python

    html_theme_options = {
        # Show breadcrumbs at the top of pages
        "show_breadcrumbs": True,

        # Include "Home" link to site_url in breadcrumbs
        "show_home_breadcrumb": True,
    }

SEO Options
~~~~~~~~~~~

Every page includes a meta description, Open Graph tags (``og:title``,
``og:description``, ``og:type``, ``og:site_name``, plus ``og:url`` and
``og:image`` when available), Twitter Card tags (``twitter:card``,
``twitter:title``, ``twitter:description``, plus ``twitter:site`` and
``twitter:image`` when configured), and - when a page URL can be resolved - a
``<link rel="canonical">``.

.. warning::

   Set ``docs_base_url`` to the URL where *your* documentation is published.
   The canonical and ``og:url`` tags are built from ``docs_base_url``, and when
   it is unset they fall back to ``site_url`` - whose default is
   ``https://mcginniscommawill.com``. A project that configures neither will
   publish canonical URLs pointing at a domain it does not control, which can
   hurt the documentation site's search ranking.

.. code-block:: python

    html_theme_options = {
        # Where these docs are published - used for canonical and og:url
        "docs_base_url": "https://user.github.io/project/",

        # Absolute URL of the social preview image (og:image / twitter:image)
        "og_image": "https://user.github.io/project/_static/social-card.png",

        # Handle used for twitter:site
        "twitter_site": "@username",
    }

If you already set Sphinx's own ``html_baseurl``, the canonical and ``og:url``
tags come from that instead and ``docs_base_url`` is not needed. If
``docs_base_url``, ``site_url``, and ``html_baseurl`` are all empty, no
canonical or ``og:url`` tag is emitted at all.

Complete Example
----------------

Here's a complete ``conf.py`` configuration for a standalone docs site:

.. code-block:: python

    import json

    html_theme = "wabi_sphinx_theme"

    html_theme_options = {
        # Branding
        "site_title": "My Project",
        "site_url": "",  # Empty for standalone docs

        # Simple nav with just docs
        "nav_links": "[]",
        "nav_show_docs_link": True,
        "nav_docs_label": "Documentation",

        # Footer
        "footer_links": json.dumps([
            {"name": "GitHub", "url": "https://github.com/user/project"},
        ]),

        # Breadcrumbs
        "show_breadcrumbs": True,
        "show_home_breadcrumb": False,
    }

    pygments_style = "wabi_sphinx_theme.pygments_style.WabiStyle"

Example: Matching mcginniscommawill.com
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To match the default configuration (mcginniscommawill.com):

.. code-block:: python

    import json

    html_theme = "wabi_sphinx_theme"

    html_theme_options = {
        "site_title": "McGinnis, Will",
        "site_url": "https://mcginniscommawill.com",

        "nav_links": json.dumps([
            {"name": "Guides", "url": "/guides/"},
            {"name": "Topics", "url": "/topics/"},
            {"name": "Blog", "url": "/posts/"},
            {"name": "About", "url": "/about/"},
            {"name": "Free Coffee", "url": "/coffee/"},
            {"name": "OSS", "url": "/oss/"},
        ]),
        "nav_show_docs_link": True,
        "nav_docs_label": "Docs",

        "footer_links": json.dumps([
            {"name": "GitHub", "url": "https://github.com/wdm0006"},
            {"name": "LinkedIn", "url": "https://www.linkedin.com/in/wmcginnis/"},
            {"name": "Twitter", "url": "https://x.com/willmcginniser"},
        ]),

        "show_breadcrumbs": True,
        "show_home_breadcrumb": True,
    }

Syntax Highlighting
-------------------

The theme includes a custom Pygments style that matches the warm aesthetic.
To use it, add to your ``conf.py``::

    pygments_style = "wabi_sphinx_theme.pygments_style.WabiStyle"

The style uses these colors:

- **Comments**: ``#8a8580`` (muted gray, italic)
- **Keywords**: ``#e9a872`` (warm orange)
- **Strings**: ``#a8c97f`` (sage green)
- **Numbers**: ``#d4a59e`` (dusty rose)
- **Errors**: ``#e85d5d`` (red)

All Options Reference
---------------------

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Option
     - Default
     - Description
   * - ``site_title``
     - "McGinnis, Will"
     - Site title shown in the header
   * - ``site_url``
     - "https://mcginniscommawill.com"
     - Base URL for nav links (empty for standalone docs)
   * - ``nav_links``
     - (see defaults)
     - JSON array of navigation links
   * - ``nav_show_docs_link``
     - True
     - Show "Docs" link in navigation
   * - ``nav_docs_label``
     - "Docs"
     - Label for the docs navigation link
   * - ``footer_links``
     - (see defaults)
     - JSON array of footer links
   * - ``footer_copyright``
     - ""
     - Custom copyright (uses Sphinx's if empty)
   * - ``show_breadcrumbs``
     - True
     - Show breadcrumb navigation
   * - ``show_home_breadcrumb``
     - True
     - Include "Home" link in breadcrumbs
   * - ``docs_base_url``
     - ""
     - Base URL of the published docs, used for canonical and ``og:url``
       (falls back to ``site_url``)
   * - ``og_image``
     - ""
     - Absolute URL of the image used for ``og:image`` and ``twitter:image``
   * - ``twitter_site``
     - ""
     - Handle used for ``twitter:site``, e.g. ``@username``
