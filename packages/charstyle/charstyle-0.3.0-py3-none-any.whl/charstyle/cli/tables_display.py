#!/usr/bin/env python3
"""
Display functions for table examples.
"""

from charstyle import Align, Style, styled, tabled


def example_header(text: str) -> str:
    """Display a standardized example header with consistent styling."""
    return styled(f"\n{text}", (Style.BOLD, Style.UNDERLINE, Style.BRIGHT_WHITE))


def show_basic_table() -> None:
    """Show a basic table example."""
    print(example_header("Basic Table Example"))

    headers = ["ID", "Name", "Department", "Status"]
    rows = [
        ["1", "Alice Smith", "Engineering", "Active"],
        ["2", "Bob Johnson", "Marketing", "Inactive"],
        ["3", "Carol Williams", "Finance", "Active"],
    ]

    print("\nSimple table with default settings (Unicode borders):")
    print(tabled(headers, rows))


def show_styled_table() -> None:
    """Show a styled table example."""
    print(example_header("Styled Table Example"))

    headers = ["ID", "Name", "Department", "Status"]
    rows = [
        ["1", "Alice Smith", "Engineering", "Active"],
        ["2", "Bob Johnson", "Marketing", "Inactive"],
        ["3", "Carol Williams", "Finance", "Active"],
    ]

    print("\nStyled table with custom widths and alignments:")
    print(
        tabled(
            headers,
            rows,
            widths=[7, 20, 17, 14],
            alignments=[Align.CENTER, Align.LEFT, Align.LEFT, Align.CENTER],
        )
    )


def show_conditional_formatting() -> None:
    """Show a table with conditional formatting."""
    print(example_header("Conditional Formatting Example"))

    headers = ["ID", "Name", "Department", "Status"]
    rows = [
        ["1", "Alice Smith", "Engineering", "Active"],
        ["2", "Bob Johnson", "Marketing", "Inactive"],
        ["3", "Carol Williams", "Finance", "Active"],
        ["4", "Dave Brown", "Engineering", "On Leave"],
    ]

    def cell_formatter(row: int, col: int, value: str) -> str | None:
        # Format ID column with bold cyan (except header)
        if col == 0 and row >= 0:
            return styled(value, (Style.CYAN, Style.BOLD), align=Align.CENTER)

        # Format Department column with different colors based on value
        elif col == 2:
            if value == "Engineering":
                return styled(value, Style.BLUE, align=Align.CENTER)
            elif value == "Marketing":
                return styled(value, Style.MAGENTA, align=Align.CENTER)
            elif value == "Finance":
                return styled(value, Style.GREEN, align=Align.CENTER)

        # Format Status column with different colors based on value
        elif col == 3:
            if value == "Active":
                return styled(value, (Style.GREEN, Style.BOLD))
            elif value == "Inactive":
                return styled(value, (Style.RED, Style.BOLD))
            else:
                return styled(value, (Style.YELLOW, Style.BOLD))

        # Return None for other cells to use default formatting
        return None

    print("\nTable with conditional formatting based on cell values:")
    print(
        tabled(
            headers,
            rows,
            widths=[7, 20, 17, 14],
            alignments=[Align.CENTER, Align.LEFT, Align.CENTER, Align.CENTER],
            borders=True,
            cell_formatter=cell_formatter,
        )
    )


def show_table_styles() -> None:
    """Show different table styles."""
    print(example_header("Table Styles Example"))

    headers = ["ID", "Name", "Department", "Status"]
    rows = [
        ["1", "Alice Smith", "Engineering", "Active"],
        ["2", "Bob Johnson", "Marketing", "Inactive"],
    ]

    print("\nDefault style (Unicode borders with header separator):")
    print(tabled(headers, rows))

    print("\nCompact style (no borders):")
    print(tabled(headers, rows, style="compact", borders=False))

    print("\nThin style (Unicode borders, no header separator):")
    print(tabled(headers, rows, style="thin"))


def show_row_highlighting() -> None:
    """Show a table with row highlighting."""
    print(example_header("Row Highlighting Example"))

    headers = ["ID", "Name", "Department", "Status"]
    rows = [
        ["1", "Alice Smith", "Engineering", "Active"],
        ["2", "Bob Johnson", "Marketing", "Inactive"],
        ["3", "Carol Williams", "Finance", "Active"],
        ["4", "Dave Brown", "Engineering", "On Leave"],
    ]

    print("\nTable with highlighted rows:")
    print(
        tabled(
            headers,
            rows,
            widths=[7, 20, 17, 14],
            alignments=[Align.CENTER, Align.LEFT, Align.LEFT, Align.CENTER],
            highlight_rows=[1, 3],  # Highlight rows at index 1 and 3 (second and fourth rows)
        )
    )


def show_alignment_options() -> None:
    """Show different alignment options for table columns."""
    print(example_header("Column Alignment Options"))

    headers = ["Left", "Center", "Right"]
    rows = [
        ["Left text", "Center text", "Right text"],
        ["Short", "Medium text", "Longer text"],
        ["123", "456", "789"],
    ]

    print("\nTable with different alignment options for each column:")
    print(
        tabled(
            headers, rows, widths=[15, 15, 15], alignments=[Align.LEFT, Align.CENTER, Align.RIGHT]
        )
    )


def show_header_styling() -> None:
    """Show different header styling options."""
    print(example_header("Header Styling Options"))

    headers = ["ID", "Name", "Department", "Status"]
    rows = [
        ["1", "Alice Smith", "Engineering", "Active"],
        ["2", "Bob Johnson", "Marketing", "Inactive"],
    ]

    print("\nBold headers (default):")
    print(tabled(headers, rows, header_style=Style.BOLD))

    print("\nUnderlined headers:")
    print(tabled(headers, rows, header_style=Style.UNDERLINE))

    print("\nBold and colored headers:")
    print(tabled(headers, rows, header_style=(Style.BOLD, Style.CYAN)))


def show_specific_style(style: str) -> None:
    """
    Show a specific table style example.

    Args:
        style: The style to show ("default", "compact", or "thin")
    """
    print(example_header(f"Charstyle Table Style: {style.capitalize()}"))
    print(f"This demonstrates the '{style}' table style in charstyle.\n")

    headers = ["ID", "Name", "Department", "Status"]
    rows = [
        ["1", "Alice Smith", "Engineering", "Active"],
        ["2", "Bob Johnson", "Marketing", "Inactive"],
        ["3", "Carol Williams", "Finance", "Active"],
    ]

    if style == "default":
        print("\nDefault style (Unicode borders with header separator):")
        print(
            tabled(
                headers,
                rows,
                widths=[5, 15, 15, 10],
                alignments=[Align.CENTER, Align.LEFT, Align.LEFT, Align.CENTER],
            )
        )

        print("\nFeatures:")
        print("- Unicode borders for a professional look")
        print("- Header separator line for clear distinction")
        print("- Bold headers for emphasis")
        print("- Customizable column widths and alignments")

    elif style == "compact":
        print("\nCompact style (no borders):")
        print(
            tabled(
                headers,
                rows,
                style="compact",
                borders=False,
                widths=[5, 15, 15, 10],
                alignments=[Align.CENTER, Align.LEFT, Align.LEFT, Align.CENTER],
            )
        )

        print("\nFeatures:")
        print("- No borders for a minimal look")
        print("- Bold and underlined headers for distinction")
        print("- Space-efficient format")
        print("- Ideal for terminal output where space is limited")

    elif style == "thin":
        print("\nThin style (Unicode borders, no header separator):")
        print(
            tabled(
                headers,
                rows,
                style="thin",
                widths=[5, 15, 15, 10],
                alignments=[Align.CENTER, Align.LEFT, Align.LEFT, Align.CENTER],
            )
        )

        print("\nFeatures:")
        print("- Unicode borders for structure")
        print("- No header separator for a cleaner look")
        print("- Bold and underlined headers for emphasis")
        print("- Perfect for data visualization and continuous data flow")
        print("- Good balance between structure and simplicity")


def show_tables() -> None:
    """Show all table examples."""
    print(example_header("Charstyle Table Examples"))
    print("This demonstrates the various table formatting capabilities of charstyle.\n")

    show_basic_table()
    show_styled_table()
    show_conditional_formatting()
    show_table_styles()
    show_row_highlighting()
    show_alignment_options()
    show_header_styling()


if __name__ == "__main__":
    show_tables()
