"""
Core module for the charstyle library.

This module provides the main styled function for applying styles to text.
"""

import functools
import os
import re
import sys

from charstyle.align import Align

# Import the style enum
from charstyle.styles import Style

# Type alias for style parameters
StyleType = Style | tuple[Style, ...]

# Global cached color support flag
# None means not yet determined
_SUPPORTS_COLOR: bool | None = None

# Regular expression to match ANSI escape codes
ANSI_ESCAPE_RE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def get_visible_length(text: str) -> int:
    """
    Calculate the visible length of a string by excluding ANSI escape codes.

    Args:
        text (str): The text to measure

    Returns:
        int: The visible length of the text
    """
    # Remove ANSI escape codes before calculating length
    return len(ANSI_ESCAPE_RE.sub("", text))


@functools.lru_cache(maxsize=1)
def supports_color() -> bool:
    """
    Check if the terminal supports color.

    Returns:
        bool: True if the terminal supports color, False otherwise
    """
    global _SUPPORTS_COLOR

    # Return cached value if already determined
    if _SUPPORTS_COLOR is not None:
        return _SUPPORTS_COLOR

    # Check for NO_COLOR environment variable
    if os.environ.get("NO_COLOR", "") != "":
        _SUPPORTS_COLOR = False
        return False

    # Check for FORCE_COLOR environment variable
    if os.environ.get("FORCE_COLOR", "") != "":
        _SUPPORTS_COLOR = True
        return True

    # Check if stdout is a TTY
    if hasattr(sys.stdout, "isatty") and sys.stdout.isatty():
        _SUPPORTS_COLOR = True
        return True

    _SUPPORTS_COLOR = False
    return False


def styled(
    text: str,
    style: StyleType | None = None,
    width: int | None = None,
    align: Align = Align.LEFT,
    fill_char: str = " ",
) -> str:
    """
    Apply styles to text using ANSI escape sequences.

    Args:
        text (str): The text to style
        style (Style, tuple): A style enum value or tuple of style enum values
        width (int, optional): Fixed width for the output text
        align (Align, optional): Alignment of the text within the fixed width
        fill_char (str, optional): Character used for filling the fixed width

    Returns:
        str: The styled text
    """
    if not text:
        return text

    # Apply alignment and width if specified
    if width is not None:
        # Calculate the visible length (excluding ANSI escape codes)
        visible_length = get_visible_length(text)
        padding_needed = max(0, width - visible_length)

        if align == Align.LEFT:
            # For left alignment, add padding to the right
            text = text + (fill_char * padding_needed)
        elif align == Align.RIGHT:
            # For right alignment, add padding to the left
            text = (fill_char * padding_needed) + text
        elif align == Align.CENTER:
            # For center alignment, add padding to both sides
            left_padding = padding_needed // 2
            right_padding = padding_needed - left_padding
            text = (fill_char * left_padding) + text + (fill_char * right_padding)

    if not style:
        return text

    # Use the cached color support value
    if not supports_color():
        return text

    # Convert single style to tuple
    styles = style if isinstance(style, tuple) else (style,)

    # Build the style string
    style_str = ";".join(s.value for s in styles)

    # Apply the style
    return f"\033[{style_str}m{text}\033[0m"
