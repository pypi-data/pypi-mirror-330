#!/usr/bin/env python3
"""
Example script demonstrating the table functionality of the charstyle library.
"""

from charstyle import Align, Style, styled, tabled


def main() -> None:
    """
    Demonstrate table functionality of charstyle.
    """
    # Sample data for tables
    headers = ["ID", "Name", "Department", "Status"]
    rows = [
        ["1", "Alice Smith", "Engineering", "Active"],
        ["2", "Bob Johnson", "Marketing", "Inactive"],
        ["3", "Carol Williams", "Finance", "Active"],
        ["4", "Dave Brown", "Engineering", "On Leave"],
    ]

    print("\n=== Simple Table ===")
    # Simple table with default settings
    print(tabled(headers, rows))

    print("\n=== Styled Table with Custom Widths and Alignments ===")
    # Styled table with custom column widths and alignments
    print(
        tabled(
            headers,
            rows,
            column_styles=[Style.BOLD, Style.GREEN, Style.BLUE, Style.YELLOW],
            header_style=Style.BOLD,
            widths=[5, 20, 15, 12],
            alignments=[Align.CENTER, Align.LEFT, Align.LEFT, Align.CENTER],
            borders=True,
        )
    )

    print("\n=== Table with Highlighting ===")
    # Table with custom fill characters and highlighting
    highlighted_rows = [0, 2]  # Highlight rows 1 and 3
    print(
        tabled(
            headers,
            rows,
            header_style=Style.BOLD,
            widths=[5, 20, 15, 10],
            alignments=[Align.CENTER, Align.LEFT, Align.LEFT, Align.CENTER],
            borders=True,
            highlight_rows=highlighted_rows,
            highlight_style=Style.YELLOW,
        )
    )

    print("\n=== Table with Conditional Formatting ===")

    # Table with conditional formatting based on cell values
    def status_formatter(row, col, value):
        if col == 3:  # Status column
            if value == "Active":
                return styled(value, Style.GREEN, align=Align.CENTER)
            elif value == "Inactive":
                return styled(value, Style.RED, align=Align.CENTER)
            else:
                return styled(value, Style.YELLOW, align=Align.CENTER)
        return None

    print(
        tabled(
            headers,
            rows,
            header_style=Style.BOLD,
            widths=[5, 20, 15, 10],
            cell_formatter=status_formatter,
            borders=True,
        )
    )

    print("\n=== Compact Table Style ===")
    # Compact table style
    print(tabled(headers, rows, style="compact", header_style=Style.UNDERLINE))

    print("\n=== ASCII-art Style Table ===")
    # ASCII-art style table
    print(tabled(headers, rows, style="ascii", header_style=Style.BOLD))


if __name__ == "__main__":
    main()
