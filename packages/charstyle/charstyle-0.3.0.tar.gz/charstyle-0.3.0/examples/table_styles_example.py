#!/usr/bin/env python3
"""
Example demonstrating the different table styles available in charstyle.
"""

from charstyle import Align, Style, styled, tabled


def main():
    """Demonstrate the different table styles in charstyle."""
    print(styled("Table Styles in charstyle", (Style.BOLD, Style.UNDERLINE)))
    print("\nThis example demonstrates the three table styles available in charstyle.\n")

    # Sample data
    headers = ["ID", "Name", "Department", "Status"]
    rows = [
        ["1", "Alice Smith", "Engineering", "Active"],
        ["2", "Bob Johnson", "Marketing", "Inactive"],
        ["3", "Carol Williams", "Finance", "Active"],
    ]

    # Default style (Unicode borders with header separator)
    print(styled("\nDefault Style", Style.BOLD))
    print("Unicode borders with header separator:")
    print(
        tabled(
            headers,
            rows,
            widths=[5, 15, 15, 10],
            alignments=[Align.CENTER, Align.LEFT, Align.LEFT, Align.CENTER],
        )
    )

    # Compact style (no borders, underlined headers)
    print(styled("\nCompact Style", Style.BOLD))
    print("No borders, with bold and underlined headers:")
    print(
        tabled(
            headers,
            rows,
            widths=[5, 15, 15, 10],
            alignments=[Align.CENTER, Align.LEFT, Align.LEFT, Align.CENTER],
            style="compact",
            borders=False,
        )
    )

    # Thin style (Unicode borders, no header separator)
    print(styled("\nThin Style", Style.BOLD))
    print("Unicode borders, no header separator, with bold and underlined headers:")
    print(
        tabled(
            headers,
            rows,
            widths=[5, 15, 15, 10],
            alignments=[Align.CENTER, Align.LEFT, Align.LEFT, Align.CENTER],
            style="thin",
        )
    )

    # Usage tips
    print(styled("\nUsage Tips", Style.BOLD))
    print("- Default style: Best for formal data presentation")
    print("- Compact style: Ideal for minimal, space-efficient output")
    print("- Thin style: Perfect for data visualization and continuous data flow")


if __name__ == "__main__":
    main()
