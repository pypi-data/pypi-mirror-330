#!/usr/bin/env python3
"""
Example script demonstrating the alignment and width features of the charstyle library.
"""

from charstyle import Align, Style, styled


def main() -> None:
    """
    Demonstrate alignment and width features of charstyle.
    """
    print("\n=== Fixed Width Examples ===")

    # Basic alignment examples
    print(styled("Default left align", Style.GREEN, width=30))
    print(styled("Right aligned", Style.YELLOW, width=30, align=Align.RIGHT))
    print(styled("Center aligned", Style.CYAN, width=30, align=Align.CENTER))

    print("\n=== Custom Fill Character Examples ===")

    # Custom fill character examples
    print(styled("Header", Style.BOLD, width=20, fill_char="-", align=Align.CENTER))
    print(styled("Title", Style.UNDERLINE, width=40, fill_char="=", align=Align.CENTER))

    print("\n=== Practical Examples ===")

    # Table-like formatting
    headers = [
        styled("ID", Style.BOLD, width=5, align=Align.CENTER),
        styled("Name", Style.BOLD, width=20, align=Align.CENTER),
        styled("Status", Style.BOLD, width=15, align=Align.CENTER),
    ]
    print("".join(headers))

    # Separator line
    print(styled("", None, width=40, fill_char="-"))

    # Table rows
    rows = [
        [
            styled("1", None, width=5, align=Align.CENTER),
            styled("Project Alpha", None, width=20, align=Align.LEFT),
            styled("Active", Style.GREEN, width=15, align=Align.CENTER),
        ],
        [
            styled("2", None, width=5, align=Align.CENTER),
            styled("Project Beta", None, width=20, align=Align.LEFT),
            styled("Pending", Style.YELLOW, width=15, align=Align.CENTER),
        ],
        [
            styled("3", None, width=5, align=Align.CENTER),
            styled("Project Gamma", None, width=20, align=Align.LEFT),
            styled("Failed", Style.RED, width=15, align=Align.CENTER),
        ],
    ]

    for row in rows:
        print("".join(row))


if __name__ == "__main__":
    main()
