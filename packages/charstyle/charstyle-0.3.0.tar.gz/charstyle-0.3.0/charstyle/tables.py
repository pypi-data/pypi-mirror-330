"""
Tables module for the charstyle library.

This module provides the tabled function for creating formatted tables.
"""

from collections.abc import Callable
from typing import Any

from charstyle.align import Align
from charstyle.charstyle import get_visible_length, styled
from charstyle.styles import Style

# Type aliases
StyleType = Style | tuple[Style, ...] | None
CellFormatterType = Callable[[int, int, Any], str | None]

# Unicode box drawing characters
BOX_HORIZONTAL = "─"
BOX_VERTICAL = "│"
BOX_TOP_LEFT = "┌"
BOX_TOP_RIGHT = "┐"
BOX_BOTTOM_LEFT = "└"
BOX_BOTTOM_RIGHT = "┘"
BOX_VERTICAL_RIGHT = "├"
BOX_VERTICAL_LEFT = "┤"
BOX_HORIZONTAL_DOWN = "┬"
BOX_HORIZONTAL_UP = "┴"
BOX_CROSS = "┼"


def _calculate_column_widths(
    headers: list[str], rows: list[list[str]], specified_widths: list[int] | None = None
) -> list[int]:
    """
    Calculate column widths based on content and specified widths.

    Args:
        headers: List of header strings
        rows: List of rows, where each row is a list of strings
        specified_widths: Optional list of specified column widths

    Returns:
        List of column widths
    """
    if specified_widths and len(specified_widths) == len(headers):
        return specified_widths

    # Initialize with header lengths
    widths = [len(str(h)) for h in headers]

    # Update with row content lengths
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(str(cell)))

    # Apply specified widths where provided
    if specified_widths:
        for i, width in enumerate(specified_widths):
            if i < len(widths):
                widths[i] = width

    return widths


def _get_cell_content(
    value: Any,
    col_index: int,
    row_index: int,
    width: int,
    alignment: Align = Align.LEFT,
    style: StyleType = None,
    cell_formatter: CellFormatterType | None = None,
) -> str:
    """
    Format a cell's content with styling and alignment.

    Args:
        value: Cell value
        col_index: Column index
        row_index: Row index
        width: Column width
        alignment: Text alignment
        style: Style to apply
        cell_formatter: Optional formatter function

    Returns:
        Formatted cell content
    """
    str_value = str(value)

    # Apply cell formatter if provided
    if cell_formatter:
        formatted = cell_formatter(row_index, col_index, value)
        if formatted is not None:
            # For formatted content, calculate the visible length and apply padding
            visible_length = get_visible_length(formatted)
            padding_needed = max(0, width - visible_length)

            if alignment == Align.LEFT:
                return formatted + (" " * padding_needed)
            elif alignment == Align.RIGHT:
                return (" " * padding_needed) + formatted
            elif alignment == Align.CENTER:
                left_padding = padding_needed // 2
                right_padding = padding_needed - left_padding
                return (" " * left_padding) + formatted + (" " * right_padding)

    # Apply styling and alignment using the styled function
    return styled(str_value, style, width=width, align=alignment)


def tabled(
    headers: list[str],
    rows: list[list[Any]],
    column_styles: list[StyleType] | None = None,
    header_style: StyleType = Style.BOLD,
    widths: list[int] | None = None,
    alignments: list[Align] | None = None,
    borders: bool = True,
    highlight_rows: list[int] | None = None,
    highlight_style: StyleType = Style.REVERSE,
    cell_formatter: CellFormatterType | None = None,
    style: str = "default",
) -> str:
    """
    Create a formatted table with headers and rows.

    Args:
        headers: List of header strings
        rows: List of rows, where each row is a list of values
        column_styles: Optional list of styles to apply to each column
        header_style: Style to apply to the header row
        widths: Optional list of column widths
        alignments: Optional list of column alignments
        borders: Whether to display borders
        highlight_rows: Optional list of row indices to highlight
        highlight_style: Style to apply to highlighted rows
        cell_formatter: Optional function to format cell values
        style: Table style ("default", "compact", or "thin")

    Returns:
        Formatted table as a string
    """
    if not headers or not rows:
        return ""

    # Calculate column widths
    col_widths = _calculate_column_widths(headers, rows, widths)
    num_cols = len(headers)

    # Set default alignments if not provided
    if not alignments:
        alignments = [Align.LEFT] * num_cols
    elif len(alignments) < num_cols:
        alignments.extend([Align.LEFT] * (num_cols - len(alignments)))

    # Set default column styles if not provided
    if not column_styles:
        column_styles = [None] * num_cols
    elif len(column_styles) < num_cols:
        column_styles.extend([None] * (num_cols - len(column_styles)))

    # Initialize highlight rows
    highlight_rows = highlight_rows or []

    # Initialize result
    result = []

    # Determine border style
    if borders:
        # Create Unicode box borders
        top_border = BOX_TOP_LEFT
        for i, width in enumerate(col_widths):
            top_border += BOX_HORIZONTAL * (width + 2)
            if i < len(col_widths) - 1:
                top_border += BOX_HORIZONTAL_DOWN
        top_border += BOX_TOP_RIGHT

        mid_border = BOX_VERTICAL_RIGHT
        for i, width in enumerate(col_widths):
            mid_border += BOX_HORIZONTAL * (width + 2)
            if i < len(col_widths) - 1:
                mid_border += BOX_CROSS
        mid_border += BOX_VERTICAL_LEFT

        bottom_border = BOX_BOTTOM_LEFT
        for i, width in enumerate(col_widths):
            bottom_border += BOX_HORIZONTAL * (width + 2)
            if i < len(col_widths) - 1:
                bottom_border += BOX_HORIZONTAL_UP
        bottom_border += BOX_BOTTOM_RIGHT

        vertical_border = BOX_VERTICAL
    else:
        top_border = mid_border = bottom_border = ""
        vertical_border = " "

    # Add top border if needed
    if borders and top_border:
        result.append(top_border)

    # Add header row
    header_cells = []
    actual_header_style: StyleType
    if style == "compact":
        actual_header_style = (Style.BOLD, Style.UNDERLINE)
    elif style == "thin":
        actual_header_style = (Style.BOLD, Style.UNDERLINE)
    else:
        actual_header_style = header_style

    for i, header in enumerate(headers[:num_cols]):
        width = col_widths[i]
        alignment = alignments[i]
        header_cells.append(_get_cell_content(header, i, -1, width, alignment, actual_header_style))

    if borders:
        result.append(
            f"{vertical_border} "
            + f" {vertical_border} ".join(header_cells)
            + f" {vertical_border}"
        )
    elif style == "compact":
        result.append(" ".join(header_cells))
    else:
        result.append(" ".join(header_cells))

    # Add separator after header if needed
    if borders and mid_border and style != "compact" and style != "thin":
        result.append(mid_border)

    # Add data rows
    for row_idx, row in enumerate(rows):
        row_style = highlight_style if row_idx in highlight_rows else None
        row_cells = []

        for col_idx, cell in enumerate(row[:num_cols]):
            width = col_widths[col_idx]
            alignment = alignments[col_idx]
            cell_style = row_style or column_styles[col_idx]

            # Get the cell content with appropriate styling and width
            cell_content = _get_cell_content(
                cell, col_idx, row_idx, width, alignment, cell_style, cell_formatter
            )

            row_cells.append(cell_content)

        if borders:
            result.append(
                f"{vertical_border} "
                + f" {vertical_border} ".join(row_cells)
                + f" {vertical_border}"
            )
        else:
            result.append(" ".join(row_cells))

    # Add bottom border if needed
    if borders and bottom_border:
        result.append(bottom_border)

    return "\n".join(result)
