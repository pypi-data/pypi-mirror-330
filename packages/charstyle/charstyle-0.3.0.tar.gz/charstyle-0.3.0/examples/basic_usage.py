#!/usr/bin/env python3
"""
Example script demonstrating the basic usage of the charstyle library.
"""

from charstyle import Style, styled


def main() -> None:
    """
    Demonstrate basic charstyle features.
    """
    print("\n=== Basic Color Examples ===")

    # Using color constants directly
    print(styled("This is red text", Style.RED))
    print(styled("This is green text", Style.GREEN))
    print(styled("This is blue text", Style.BLUE))
    print(styled("This is cyan text", Style.CYAN))

    # Using text style constants
    print(styled("This is bold text", Style.BOLD))
    print(styled("This is italic text", Style.ITALIC))
    print(styled("This is underlined text", Style.UNDERLINE))
    print(styled("This is strikethrough text", Style.STRIKE))

    # Combining color and style with tuples
    print(styled("This is bold red text", (Style.RED, Style.BOLD)))
    print(styled("This is italic blue text", (Style.BLUE, Style.ITALIC)))

    # Using multiple styles with tuple
    print(styled("This is bold and underlined text", (Style.BOLD, Style.UNDERLINE)))

    print("\n=== Predefined Style Examples ===")

    # Create predefined styles as tuples
    error_style = (Style.BRIGHT_RED, Style.BOLD)
    warning_style = (Style.YELLOW, Style.ITALIC)
    success_style = (Style.GREEN, Style.BOLD)

    # Apply predefined styles
    print(styled("This is an error message", error_style))
    print(styled("This is a warning message", warning_style))
    print(styled("This is a success message", success_style))

    print("\n=== Background Color Examples ===")

    # Using background colors
    print(styled("Text with red background", Style.BG_RED))
    print(styled("Text with green background", Style.BG_GREEN))

    # Combining foreground and background colors
    print(styled("White text on blue background", (Style.WHITE, Style.BG_BLUE)))
    print(styled("Black text on bright yellow background", (Style.BLACK, Style.BG_BRIGHT_YELLOW)))

    # Complex styling
    print(
        styled(
            "Bold italic text with yellow foreground and blue background",
            (Style.BOLD, Style.ITALIC, Style.YELLOW, Style.BG_BLUE),
        )
    )

    # Alternative complex styling with good contrast
    print(
        styled(
            "Bold italic text with white on red background",
            (Style.BOLD, Style.ITALIC, Style.WHITE, Style.BG_RED),
        )
    )


if __name__ == "__main__":
    main()
