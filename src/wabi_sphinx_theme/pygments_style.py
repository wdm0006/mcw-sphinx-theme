"""
Wabi Pygments Style
==================

A warm, earthy syntax highlighting theme matching the Wabi aesthetic.
Dark background (#2d2a26) with cream text and terracotta/sage accents.
"""

from pygments.style import Style
from pygments.token import (
    Comment,
    Error,
    Generic,
    Keyword,
    Literal,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Text,
    Token,
    Whitespace,
)


class WabiStyle(Style):
    """
    Wabi Pygments style - warm, earthy colors on dark background.
    Matches the Wabi Hugo/Sphinx theme aesthetic.
    """

    name = "wabi"

    # Background and default colors
    background_color = "#2d2a26"
    highlight_color = "#3d3a36"
    line_number_color = "#6b6560"

    styles = {
        # Base
        Token: "#f5f2ed",
        Whitespace: "#f5f2ed",
        Text: "#f5f2ed",
        # Comments - muted gray, italic
        Comment: "italic #8a8580",
        Comment.Hashbang: "italic #8a8580",
        Comment.Multiline: "italic #8a8580",
        Comment.Preproc: "#8a8580",
        Comment.PreprocFile: "#8a8580",
        Comment.Single: "italic #8a8580",
        Comment.Special: "italic #8a8580",
        # Keywords - warm orange
        Keyword: "#e9a872",
        Keyword.Constant: "#e9a872",
        Keyword.Declaration: "#e9a872",
        Keyword.Namespace: "#e9a872",
        Keyword.Pseudo: "#e9a872",
        Keyword.Reserved: "#e9a872",
        Keyword.Type: "#d4a59e",
        # Operators
        Operator: "#f5f2ed",
        Operator.Word: "#e9a872",
        # Punctuation
        Punctuation: "#f5f2ed",
        # Names - default cream
        Name: "#f5f2ed",
        Name.Attribute: "#f5f2ed",
        Name.Builtin: "#f5f2ed",
        Name.Builtin.Pseudo: "#f5f2ed",
        Name.Class: "#f5f2ed",
        Name.Constant: "#f5f2ed",
        Name.Decorator: "#d4a59e",
        Name.Entity: "#f5f2ed",
        Name.Exception: "#e85d5d",
        Name.Function: "#f5f2ed",
        Name.Function.Magic: "#f5f2ed",
        Name.Label: "#f5f2ed",
        Name.Namespace: "#f5f2ed",
        Name.Other: "#f5f2ed",
        Name.Property: "#f5f2ed",
        Name.Tag: "#f5f2ed",
        Name.Variable: "#f5f2ed",
        Name.Variable.Class: "#f5f2ed",
        Name.Variable.Global: "#f5f2ed",
        Name.Variable.Instance: "#f5f2ed",
        Name.Variable.Magic: "#f5f2ed",
        # Strings - sage green
        String: "#a8c97f",
        String.Affix: "#a8c97f",
        String.Backtick: "#a8c97f",
        String.Char: "#a8c97f",
        String.Delimiter: "#a8c97f",
        String.Doc: "italic #8a8580",
        String.Double: "#a8c97f",
        String.Escape: "#d4a59e",
        String.Heredoc: "#a8c97f",
        String.Interpol: "#a8c97f",
        String.Other: "#a8c97f",
        String.Regex: "#a8c97f",
        String.Single: "#a8c97f",
        String.Symbol: "#a8c97f",
        # Numbers - dusty rose
        Number: "#d4a59e",
        Number.Bin: "#d4a59e",
        Number.Float: "#d4a59e",
        Number.Hex: "#d4a59e",
        Number.Integer: "#d4a59e",
        Number.Integer.Long: "#d4a59e",
        Number.Oct: "#d4a59e",
        # Literals
        Literal: "#d4a59e",
        Literal.Date: "#d4a59e",
        # Generic
        Generic: "#f5f2ed",
        Generic.Deleted: "#e85d5d",
        Generic.Emph: "italic #f5f2ed",
        Generic.Error: "#e85d5d",
        Generic.Heading: "bold #f5f2ed",
        Generic.Inserted: "#a8c97f",
        Generic.Output: "#f5f2ed",
        Generic.Prompt: "#6b6560",
        Generic.Strong: "bold #f5f2ed",
        Generic.Subheading: "bold #f5f2ed",
        Generic.Traceback: "#e85d5d",
        # Errors
        Error: "#e85d5d",
    }
