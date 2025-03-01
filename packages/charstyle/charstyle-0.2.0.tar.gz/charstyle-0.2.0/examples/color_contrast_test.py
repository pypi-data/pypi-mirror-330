#!/usr/bin/env python3
"""
Color contrast test for charstyle.

This example demonstrates all foreground and background color combinations.
"""

from charstyle import Style, styled, supports_color


def main() -> None:
    """Run the color contrast test."""
    if not supports_color():
        print("This terminal does not support color.")
        return

    # Foreground colors
    fg_colors = [
        ("BLACK", Style.BLACK),
        ("RED", Style.RED),
        ("GREEN", Style.GREEN),
        ("YELLOW", Style.YELLOW),
        ("BLUE", Style.BLUE),
        ("MAGENTA", Style.MAGENTA),
        ("CYAN", Style.CYAN),
        ("WHITE", Style.WHITE),
        ("BRIGHT_BLACK", Style.BRIGHT_BLACK),
        ("BRIGHT_RED", Style.BRIGHT_RED),
        ("BRIGHT_GREEN", Style.BRIGHT_GREEN),
        ("BRIGHT_YELLOW", Style.BRIGHT_YELLOW),
        ("BRIGHT_BLUE", Style.BRIGHT_BLUE),
        ("BRIGHT_MAGENTA", Style.BRIGHT_MAGENTA),
        ("BRIGHT_CYAN", Style.BRIGHT_CYAN),
        ("BRIGHT_WHITE", Style.BRIGHT_WHITE),
    ]

    # Background colors
    bg_colors = [
        ("BG_BLACK", Style.BG_BLACK),
        ("BG_RED", Style.BG_RED),
        ("BG_GREEN", Style.BG_GREEN),
        ("BG_YELLOW", Style.BG_YELLOW),
        ("BG_BLUE", Style.BG_BLUE),
        ("BG_MAGENTA", Style.BG_MAGENTA),
        ("BG_CYAN", Style.BG_CYAN),
        ("BG_WHITE", Style.BG_WHITE),
        ("BG_BRIGHT_BLACK", Style.BG_BRIGHT_BLACK),
        ("BG_BRIGHT_RED", Style.BG_BRIGHT_RED),
        ("BG_BRIGHT_GREEN", Style.BG_BRIGHT_GREEN),
        ("BG_BRIGHT_YELLOW", Style.BG_BRIGHT_YELLOW),
        ("BG_BRIGHT_BLUE", Style.BG_BRIGHT_BLUE),
        ("BG_BRIGHT_MAGENTA", Style.BG_BRIGHT_MAGENTA),
        ("BG_BRIGHT_CYAN", Style.BG_BRIGHT_CYAN),
        ("BG_BRIGHT_WHITE", Style.BG_BRIGHT_WHITE),
    ]

    # Print header
    print("Color Contrast Test")
    print("==================")
    print("This test shows all combinations of foreground and background colors.")
    print("The text should be readable for good contrast combinations.")
    print()

    # Print all combinations
    for fg_name, fg_color in fg_colors:
        for bg_name, bg_color in bg_colors:
            style = (fg_color, bg_color)
            text = f"{fg_name} on {bg_name}"
            print(styled(text.ljust(40), style), end=" ")
        print()


if __name__ == "__main__":
    main()
