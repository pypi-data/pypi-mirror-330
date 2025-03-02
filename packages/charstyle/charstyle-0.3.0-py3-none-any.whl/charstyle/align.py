"""
Alignment enums for the charstyle library.

This module provides alignment options for styled text.
"""

from enum import Enum


class Align(Enum):
    """
    Enum for text alignment options.

    This enum defines different alignment options for styled text when using
    fixed width formatting.
    """

    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
