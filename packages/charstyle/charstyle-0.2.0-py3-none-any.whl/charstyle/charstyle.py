"""
Core module for the charstyle library.

This module provides the main styled function for applying styles to text.
"""

import os
import sys

# Import the style enum
from charstyle.style_enum import Style

# Type alias for style parameters
StyleType = Style | tuple[Style, ...]


def styled(
    text: str,
    style: StyleType | None = None,
) -> str:
    """
    Apply styles to text using ANSI escape sequences.

    Args:
        text (str): The text to style
        style (Style, tuple): A style enum value or tuple of style enum values

    Returns:
        str: The styled text
    """
    if not text:
        return text

    if not style or not supports_color():
        return text

    # Convert single style to tuple
    styles = style if isinstance(style, tuple) else (style,)

    # Build the style string
    style_str = ";".join(s.value for s in styles)

    # Apply the style
    return f"\033[{style_str}m{text}\033[0m"


def supports_color() -> bool:
    """
    Check if the terminal supports color.

    Returns:
        bool: True if the terminal supports color, False otherwise
    """
    # Check for NO_COLOR environment variable
    if os.environ.get("NO_COLOR", "") != "":
        return False

    # Check for FORCE_COLOR environment variable
    if os.environ.get("FORCE_COLOR", "") != "":
        return True

    # Check if stdout is a TTY
    if hasattr(sys.stdout, "isatty") and sys.stdout.isatty():
        return True

    return False
