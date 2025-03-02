#!/usr/bin/env python3
"""
Example script demonstrating the requested alignment and width features.
"""

from charstyle import Align, Style, styled


def main() -> None:
    """
    Demonstrate the requested features.
    """
    # Fixed width examples
    print(styled("Default left align", Style.GREEN, width=30))
    print(styled("Right aligned", Style.YELLOW, width=30, align=Align.RIGHT))
    print(styled("Center aligned", Style.CYAN, width=30, align=Align.CENTER))

    # Custom fill character examples
    print(styled("Header", Style.BOLD, width=20, fill_char="-", align=Align.CENTER))
    print(styled("Title", Style.UNDERLINE, width=40, fill_char="=", align=Align.CENTER))


if __name__ == "__main__":
    main()
