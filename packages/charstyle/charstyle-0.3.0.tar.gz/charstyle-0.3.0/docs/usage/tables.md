# Table Formatting

The charstyle library provides a powerful `tabled()` function for creating formatted tables in the terminal. This function makes it easy to create professional-looking tables with various styling options.

## Basic Usage

The simplest way to create a table is to provide headers and rows:

```python
from charstyle import tabled, Style, Align

headers = ["ID", "Name", "Department", "Status"]
rows = [
    ["1", "Alice Smith", "Engineering", "Active"],
    ["2", "Bob Johnson", "Marketing", "Inactive"],
    ["3", "Carol Williams", "Finance", "Active"],
]

# Simple table with default settings
print(tabled(headers, rows))
```

This will produce a simple table with automatically calculated column widths:

```
ID Name           Department  Status
1  Alice Smith    Engineering Active
2  Bob Johnson    Marketing   Inactive
3  Carol Williams Finance     Active
```

## Styled Tables with Borders

You can add borders with Unicode box-drawing characters to make your tables more visually appealing:

```python
print(tabled(
    headers,
    rows,
    header_style=Style.BOLD,
    widths=[5, 20, 15, 12],
    alignments=[Align.CENTER, Align.LEFT, Align.LEFT, Align.CENTER],
    borders=True
))
```

This will produce a table with Unicode box-drawing characters, bold headers, and custom column widths and alignments:

```
┌───────┬──────────────────────┬─────────────────┬──────────────┐
│  ID   │ Name                 │ Department      │   Status     │
├───────┼──────────────────────┼─────────────────┼──────────────┤
│  1    │ Alice Smith          │ Engineering     │   Active     │
│  2    │ Bob Johnson          │ Marketing       │  Inactive    │
│  3    │ Carol Williams       │ Finance         │   Active     │
└───────┴──────────────────────┴─────────────────┴──────────────┘
```

## Row Highlighting

You can highlight specific rows in the table:

```python
highlighted_rows = [0, 2]  # Highlight rows 1 and 3
print(tabled(
    headers,
    rows,
    header_style=Style.BOLD,
    widths=[5, 20, 15, 10],
    alignments=[Align.CENTER, Align.LEFT, Align.LEFT, Align.CENTER],
    borders=True,
    highlight_rows=highlighted_rows,
    highlight_style=Style.YELLOW
))
```

This will highlight the specified rows with the given style.

## Conditional Formatting

You can apply conditional formatting to cells based on their values:

```python
def cell_formatter(row, col, value):
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

print(tabled(
    headers,
    rows,
    header_style=Style.BOLD,
    widths=[7, 20, 17, 14],
    alignments=[Align.CENTER, Align.LEFT, Align.CENTER, Align.CENTER],
    cell_formatter=cell_formatter,
    borders=True
))
```

This will apply different styles to cells based on their column and value.

## Table Styles

The `tabled()` function supports different table styles:

### Default Style

```python
print(tabled(headers, rows))
```

### Compact Style

```python
print(tabled(
    headers,
    rows,
    style="compact",
    header_style=Style.UNDERLINE
))
```

This creates a more compact table with underlined headers:

```
ID Name           Department  Status
-----------------------------------
1  Alice Smith    Engineering Active
2  Bob Johnson    Marketing   Inactive
3  Carol Williams Finance     Active
```

### Thin Style

```python
print(tabled(
    headers,
    rows,
    style="thin",
    header_style=(Style.BOLD, Style.UNDERLINE)
))
```

This creates a table with thin Unicode borders and no separator line between headers and data:

```
┌───┬───────────────┬─────────────┬─────────┐
│ID │Name           │Department   │Status   │
│1  │Alice Smith    │Engineering  │Active   │
│2  │Bob Johnson    │Marketing    │Inactive │
│3  │Carol Williams │Finance      │Active   │
└───┴───────────────┴─────────────┴─────────┘
```

## API Reference

The `tabled()` function accepts the following parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| headers | List[str] | List of header strings |
| rows | List[List[Any]] | List of rows, where each row is a list of values |
| column_styles | Optional[List[StyleType]] | Optional list of styles to apply to each column |
| header_style | StyleType | Style to apply to the header row (default: Style.BOLD) |
| widths | Optional[List[int]] | Optional list of column widths |
| alignments | Optional[List[Align]] | Optional list of column alignments |
| borders | bool | Whether to display borders with Unicode box-drawing characters (default: False) |
| highlight_rows | Optional[List[int]] | Optional list of row indices to highlight |
| highlight_style | StyleType | Style to apply to highlighted rows (default: Style.REVERSE) |
| cell_formatter | Optional[Callable] | Optional function to format cell values |
| style | str | Table style ("default", "compact", or "thin") |

The cell formatter function should have the signature:

```python
def formatter(row_index: int, col_index: int, value: Any) -> Optional[str]:
    # Return a formatted string or None to use default formatting
    if col_index == 0 and row_index > 0:  # Format the ID column (except header)
        return styled(value, (Style.CYAN, Style.BOLD))
    elif col_index == 2:  # Format the Department column
        if value == "Engineering":
            return styled(value, Style.BLUE, align=Align.CENTER)
        elif value == "Marketing":
            return styled(value, Style.MAGENTA, align=Align.CENTER)
        elif value == "Finance":
            return styled(value, Style.GREEN, align=Align.CENTER)
    # Return None for other cells to use default formatting
    return None
```

If the formatter returns None, the default formatting will be applied.
