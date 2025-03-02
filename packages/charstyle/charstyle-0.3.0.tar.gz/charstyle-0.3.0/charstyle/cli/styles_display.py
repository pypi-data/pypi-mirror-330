"""
Style display functionality for charstyle CLI.
This module provides functions to display terminal styles.
"""


def example_header(text: str) -> str:
    """Display a standardized example header with consistent styling."""
    from charstyle import Style, styled

    return styled(f"\n{text}", (Style.BOLD, Style.UNDERLINE, Style.BRIGHT_WHITE))


def show_styles() -> None:
    """Display all available terminal styles."""
    from charstyle import Align, Style, styled, supports_color

    print(example_header("charstyle Demo"))
    print("A library for styling terminal text using ANSI escape sequences")
    print()

    # Check if terminal supports colors
    if not supports_color():
        print("Your terminal does not support colors.")
        exit(1)

    # Fixed widths for consistent formatting
    style_name_width = 26  # Enough for "Style.BRIGHT_MAGENTA"
    example_width = 26  # Enough for "This is bright magenta"

    # Define all style names for different categories
    color_styles = [
        ("BLACK", Style.BLACK, "BRIGHT_BLACK", Style.BRIGHT_BLACK),
        ("RED", Style.RED, "BRIGHT_RED", Style.BRIGHT_RED),
        ("GREEN", Style.GREEN, "BRIGHT_GREEN", Style.BRIGHT_GREEN),
        ("YELLOW", Style.YELLOW, "BRIGHT_YELLOW", Style.BRIGHT_YELLOW),
        ("BLUE", Style.BLUE, "BRIGHT_BLUE", Style.BRIGHT_BLUE),
        ("MAGENTA", Style.MAGENTA, "BRIGHT_MAGENTA", Style.BRIGHT_MAGENTA),
        ("CYAN", Style.CYAN, "BRIGHT_CYAN", Style.BRIGHT_CYAN),
        ("WHITE", Style.WHITE, "BRIGHT_WHITE", Style.BRIGHT_WHITE),
    ]

    bg_styles = [
        ("BG_BLACK", Style.BG_BLACK, "BG_BRIGHT_BLACK", Style.BG_BRIGHT_BLACK),
        ("BG_RED", Style.BG_RED, "BG_BRIGHT_RED", Style.BG_BRIGHT_RED),
        ("BG_GREEN", Style.BG_GREEN, "BG_BRIGHT_GREEN", Style.BG_BRIGHT_GREEN),
        ("BG_YELLOW", Style.BG_YELLOW, "BG_BRIGHT_YELLOW", Style.BG_BRIGHT_YELLOW),
        ("BG_BLUE", Style.BG_BLUE, "BG_BRIGHT_BLUE", Style.BG_BRIGHT_BLUE),
        ("BG_MAGENTA", Style.BG_MAGENTA, "BG_BRIGHT_MAGENTA", Style.BG_BRIGHT_MAGENTA),
        ("BG_CYAN", Style.BG_CYAN, "BG_BRIGHT_CYAN", Style.BG_BRIGHT_CYAN),
        ("BG_WHITE", Style.BG_WHITE, "BG_BRIGHT_WHITE", Style.BG_BRIGHT_WHITE),
    ]

    text_styles = [
        ("BOLD", Style.BOLD),
        ("DIM", Style.DIM),
        ("ITALIC", Style.ITALIC),
        ("UNDERLINE", Style.UNDERLINE),
        ("BLINK", Style.BLINK),
        ("REVERSE", Style.REVERSE),
        ("STRIKE", Style.STRIKE),
    ]

    combinations = [
        ("BOLD + RED", (Style.BOLD, Style.RED), "This text is bold and red"),
        ("UNDERLINE + BLUE", (Style.UNDERLINE, Style.BLUE), "This text is underlined and blue"),
        (
            "BOLD + ITALIC + GREEN",
            (Style.BOLD, Style.ITALIC, Style.GREEN),
            "This text is bold, italic, and green",
        ),
        ("WHITE + BG_RED", (Style.WHITE, Style.BG_RED), "This text is white on red background"),
        (
            "BOLD + YELLOW + BG_BLUE",
            (Style.BOLD, Style.YELLOW, Style.BG_BLUE),
            "This text is bold yellow on blue background",
        ),
    ]

    predefined = [
        ("ERROR", (Style.ERROR, Style.BOLD), "This is an error message"),
        ("WARNING", (Style.WARNING, Style.BOLD), "This is a warning message"),
        ("SUCCESS", (Style.SUCCESS, Style.BOLD), "This is a success message"),
        ("INFO", (Style.INFO, Style.BOLD), "This is an info message"),
        ("DEBUG", (Style.DEBUG, Style.BOLD), "This is a debug message"),
    ]

    print(example_header("Text Colors"))
    for name, color, bright_name, bright_color in color_styles:
        regular_text = name.lower()
        regular_style = styled(
            f"Style.{name}", Style.BOLD, width=style_name_width, align=Align.LEFT
        )
        regular_example = styled(
            f"This is {regular_text}", color, width=example_width, align=Align.LEFT
        )

        bright_style = styled(
            f"Style.{bright_name}", Style.BOLD, width=style_name_width, align=Align.LEFT
        )
        bright_example = styled(
            f"This is bright {regular_text}", bright_color, width=example_width, align=Align.LEFT
        )

        print(f"{regular_style} {regular_example} | {bright_style} {bright_example}")

    print(example_header("Background Colors"))
    for name, bg, bright_name, bright_bg in bg_styles:
        base_name = name.replace("BG_", "").lower()

        # For regular background colors
        regular_style = styled(
            f"Style.{name}", Style.BOLD, width=style_name_width, align=Align.LEFT
        )
        regular_text = f"Text on {base_name} background"
        regular_example = styled(regular_text, bg, width=example_width, align=Align.LEFT)

        # For bright background colors - use the same width but different text
        bright_style = styled(
            f"Style.{bright_name}", Style.BOLD, width=style_name_width, align=Align.LEFT
        )
        bright_text = f"Text on bright {base_name} bg"  # Shortened to fit
        bright_example = styled(bright_text, bright_bg, width=example_width, align=Align.LEFT)

        print(f"{regular_style} {regular_example} | {bright_style} {bright_example}")

    print(example_header("Text Styles"))
    for name, style in text_styles:
        style_name = styled(f"Style.{name}", Style.BOLD, width=style_name_width, align=Align.LEFT)
        example = styled(
            f"This text is {name.lower()}", style, width=example_width, align=Align.LEFT
        )
        print(f"{style_name} {example}")

    print(example_header("Combinations"))
    for name, style_tuple, text in combinations:
        style_name = styled(f"Style.{name}", Style.BOLD, width=style_name_width, align=Align.LEFT)
        example = styled(text, style_tuple, width=example_width, align=Align.LEFT)
        print(f"{style_name} {example}")

    print(example_header("Predefined Styles"))
    for name, style_tuple, text in predefined:
        style_name = styled(f"Style.{name}", Style.BOLD, width=style_name_width, align=Align.LEFT)
        example = styled(text, style_tuple, width=example_width, align=Align.LEFT)
        print(f"{style_name} {example}")


if __name__ == "__main__":
    show_styles()
