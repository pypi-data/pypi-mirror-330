"""
Style display functionality for charstyle CLI.
This module provides functions to display terminal styles.
"""


def show_styles() -> None:
    """Display all available terminal styles."""
    from charstyle import Style, styled, supports_color

    # Create style functions
    def bold(text: str) -> str:
        return styled(text, Style.BOLD)

    def red(text: str) -> str:
        return styled(text, Style.RED)

    def green(text: str) -> str:
        return styled(text, Style.GREEN)

    def blue(text: str) -> str:
        return styled(text, Style.BLUE)

    def yellow(text: str) -> str:
        return styled(text, Style.YELLOW)

    def underline(text: str) -> str:
        return styled(text, Style.UNDERLINE)

    print("\n=== charstyle Demo ===")
    print("A library for styling terminal text using ANSI escape sequences")
    print()

    # Check if terminal supports colors
    if not supports_color():
        print("Your terminal does not support colors.")
        exit(1)

    print("=== Text Colors ===")
    colors = [
        ("BLACK", Style.BLACK, "BRIGHT_BLACK", Style.BRIGHT_BLACK),
        ("RED", Style.RED, "BRIGHT_RED", Style.BRIGHT_RED),
        ("GREEN", Style.GREEN, "BRIGHT_GREEN", Style.BRIGHT_GREEN),
        ("YELLOW", Style.YELLOW, "BRIGHT_YELLOW", Style.BRIGHT_YELLOW),
        ("BLUE", Style.BLUE, "BRIGHT_BLUE", Style.BRIGHT_BLUE),
        ("MAGENTA", Style.MAGENTA, "BRIGHT_MAGENTA", Style.BRIGHT_MAGENTA),
        ("CYAN", Style.CYAN, "BRIGHT_CYAN", Style.BRIGHT_CYAN),
        ("WHITE", Style.WHITE, "BRIGHT_WHITE", Style.BRIGHT_WHITE),
    ]

    # Calculate the padding needed for each color name
    # Magenta is the longest: "This text is magenta"
    max_text_length = len("This text is magenta")

    for name, color, _, bright_color in colors:
        # Pad the regular text color to match the length of magenta
        regular_text = name.lower()
        padding = " " * (max_text_length - len(f"This text is {regular_text}"))
        print(
            f"This text is {styled(regular_text, color)}{padding} | This text is {styled(f'bright {regular_text}', bright_color)}"
        )

    print("\n=== Background Colors ===")
    backgrounds = [
        ("BLACK", Style.BG_BLACK, "BRIGHT_BLACK", Style.BG_BRIGHT_BLACK),
        ("RED", Style.BG_RED, "BRIGHT_RED", Style.BG_BRIGHT_RED),
        ("GREEN", Style.BG_GREEN, "BRIGHT_GREEN", Style.BG_BRIGHT_GREEN),
        ("YELLOW", Style.BG_YELLOW, "BRIGHT_YELLOW", Style.BG_BRIGHT_YELLOW),
        ("BLUE", Style.BG_BLUE, "BRIGHT_BLUE", Style.BG_BRIGHT_BLUE),
        ("MAGENTA", Style.BG_MAGENTA, "BRIGHT_MAGENTA", Style.BG_BRIGHT_MAGENTA),
        ("CYAN", Style.BG_CYAN, "BRIGHT_CYAN", Style.BG_BRIGHT_CYAN),
        ("WHITE", Style.BG_WHITE, "BRIGHT_WHITE", Style.BG_BRIGHT_WHITE),
    ]

    for name, bg_color, _, bright_bg_color in backgrounds:
        # Pad the regular background color to match the length of magenta
        regular_text = name.lower()
        padding = " " * (max_text_length - len(f"This has a {regular_text} background"))
        print(
            f"This has a {styled('black' if name != 'BLACK' else 'white', (Style.BLACK if name != 'BLACK' else Style.WHITE, bg_color))}{padding} | "
            f"This has a {styled('black' if name != 'BLACK' else 'white', (Style.BLACK if name != 'BLACK' else Style.WHITE, bright_bg_color))} background"
        )

    print("\n=== Text Styles ===")
    styles = [
        ("BOLD", Style.BOLD),
        ("DIM", Style.DIM),
        ("ITALIC", Style.ITALIC),
        ("UNDERLINE", Style.UNDERLINE),
        ("BLINK", Style.BLINK),
        ("REVERSE", Style.REVERSE),
        ("STRIKE", Style.STRIKE),
    ]

    for name, style in styles:
        print(f"This text is {styled(name.lower(), style)}")

    print("\n=== Combinations ===")
    print(f"This text is {styled('bold and red', (Style.BOLD, Style.RED))}")
    print(f"This text is {styled('underlined and blue', (Style.UNDERLINE, Style.BLUE))}")
    print(
        f"This text is {styled('bold, italic, and green', (Style.BOLD, Style.ITALIC, Style.GREEN))}"
    )
    print(f"This text is {styled('white on red background', (Style.WHITE, Style.BG_RED))}")
    print(
        f"This text is {styled('bold yellow on blue background', (Style.BOLD, Style.YELLOW, Style.BG_BLUE))}"
    )

    print("\n=== Nesting ===")
    print(
        f"This is {styled('normal with a', Style.WHITE)} {styled('bold', Style.BOLD)} {styled('word', Style.WHITE)}"
    )
    print(
        f"This is {styled('white with a', Style.WHITE)} {styled('red', Style.RED)} {styled('word', Style.WHITE)}"
    )
    print(
        f"This is {styled('normal with', Style.WHITE)} {styled('multiple', Style.BOLD)} {styled('styled', Style.ITALIC)} {styled('words', Style.UNDERLINE)}"
    )

    print("\n=== Predefined Styles ===")
    print(f"{styled('This is an error message', (Style.RED, Style.BOLD))}")
    print(f"{styled('This is a warning message', (Style.YELLOW, Style.BOLD))}")
    print(f"{styled('This is a success message', (Style.GREEN, Style.BOLD))}")
    print(f"{styled('This is an info message', (Style.BLUE, Style.BOLD))}")
    print(f"{styled('This is a debug message', (Style.MAGENTA, Style.BOLD))}")

    print("\nFor more information, visit: https://github.com/joaompinto/charstyle")
