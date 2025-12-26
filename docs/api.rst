API Reference
=============

This page documents the Python API for the Wabi Sphinx Theme.

Module: wabi_sphinx_theme
-------------------------

.. py:module:: wabi_sphinx_theme

The main module provides the Sphinx theme entry point.

.. py:data:: __version__
   :type: str

   The current version of the theme.

.. py:function:: get_html_theme_path()

   Return the path to the theme templates.

   :returns: Path to the theme template directory
   :rtype: str

.. py:function:: setup(app)

   Sphinx extension setup function.

   :param app: The Sphinx application instance
   :type app: sphinx.application.Sphinx
   :returns: Extension metadata
   :rtype: dict

Module: wabi_sphinx_theme.pygments_style
----------------------------------------

.. py:module:: wabi_sphinx_theme.pygments_style

Custom Pygments style matching the Wabi aesthetic.

.. py:class:: WabiStyle

   A warm, earthy Pygments style with dark background.

   **Background Colors:**

   - ``background_color``: ``#2d2a26`` (dark warm gray)
   - ``highlight_color``: ``#3d3a36`` (highlighted line)

   **Token Colors:**

   - Text: ``#f5f2ed`` (cream)
   - Comments: ``#8a8580`` (muted gray, italic)
   - Keywords: ``#e9a872`` (warm orange)
   - Strings: ``#a8c97f`` (sage green)
   - Numbers: ``#d4a59e`` (dusty rose)
   - Errors: ``#e85d5d`` (red)

Example Code Block
------------------

Here's how code looks with the Wabi Pygments style:

.. code-block:: python

    def greet(name: str) -> str:
        """Return a friendly greeting."""
        # This is a comment
        message = f"Hello, {name}!"
        return message

    # Numbers and constants
    PI = 3.14159
    COUNT = 42

    if __name__ == "__main__":
        print(greet("World"))
