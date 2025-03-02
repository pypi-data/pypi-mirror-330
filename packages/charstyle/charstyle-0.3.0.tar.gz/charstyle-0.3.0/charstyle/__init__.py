"""
charstyle - A simple library for styling terminal text output using ANSI escape sequences.

This library provides functions to add color, background color, and text styles
(bold, italic, underline, etc.) to text output in terminal applications.

Requires Python 3.11+ for StrEnum support.
"""

# Import the core styling function and style enum
from charstyle.align import Align
from charstyle.charstyle import styled, supports_color

# Import the Icon enum
from charstyle.icons import Icon

# Import pattern styling functions
from charstyle.pattern_style import (
    styled_format,
    styled_pattern,
    styled_pattern_match,
    styled_split,
)
from charstyle.styles import Style
from charstyle.tables import tabled

__version__ = "0.3.0"

__all__ = [
    # Core API
    "styled",
    "Style",
    "Align",
    "supports_color",
    "tabled",
    "__version__",
    # Icon enum
    "Icon",
    # Pattern styling functions
    "styled_pattern",
    "styled_format",
    "styled_pattern_match",
    "styled_split",
    # Table functionality
]
