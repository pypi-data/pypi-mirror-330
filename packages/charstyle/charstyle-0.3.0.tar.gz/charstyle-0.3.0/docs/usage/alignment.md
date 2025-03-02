# Text Alignment and Formatting

charstyle provides powerful text alignment and formatting capabilities that allow you to create well-structured terminal output.

## Basic Alignment

You can align text within a fixed width using the `width` and `align` parameters:

```python
from charstyle import styled, Style, Align

# Left alignment (default)
print(styled("Left aligned", Style.GREEN, width=30))

# Right alignment
print(styled("Right aligned", Style.YELLOW, width=30, align=Align.RIGHT))

# Center alignment
print(styled("Center aligned", Style.CYAN, width=30, align=Align.CENTER))
```

This produces:

```
Left aligned
                  Right aligned
        Center aligned
```

## Custom Fill Characters

By default, spaces are used to fill the width, but you can specify a custom fill character:

```python
from charstyle import styled, Style, Align

# Create a header with dashes
print(styled("Header", Style.BOLD, width=20, fill_char="-", align=Align.CENTER))

# Create a title with equals signs
print(styled("Title", Style.UNDERLINE, width=40, fill_char="=", align=Align.CENTER))
```

This produces:

```
-------Header-------
=================Title==================
```

## Creating Tables

You can use alignment features to create simple tables:

```python
from charstyle import styled, Style, Align

# Table headers
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
```

This produces a nicely formatted table:

```
  ID         Name             Status
----------------------------------------
  1  Project Alpha            Active
  2  Project Beta            Pending
  3  Project Gamma            Failed
```

## Practical Applications

### Creating Headers and Separators

```python
from charstyle import styled, Style, Align

# Main header
print(styled("SYSTEM STATUS", Style.BOLD, width=50, fill_char="=", align=Align.CENTER))

# Section header
print(styled("Network", Style.BOLD, width=30, fill_char="-", align=Align.CENTER))

# Content with alignment
print(styled("Status:", Style.BOLD, width=15) + styled("Online", Style.GREEN))
print(styled("Latency:", Style.BOLD, width=15) + styled("24ms", Style.CYAN))
print(styled("Uptime:", Style.BOLD, width=15) + styled("99.9%", Style.BLUE))
```

### Creating Progress Bars

```python
from charstyle import styled, Style, Align

def progress_bar(percent, width=40):
    """Create a styled progress bar."""
    filled = int(width * percent / 100)
    empty = width - filled

    bar = styled("█" * filled, Style.GREEN) + styled("░" * empty, Style.DIM)
    return f"{bar} {styled(f'{percent}%', Style.BOLD)}"

# Display progress bars
print(progress_bar(25, 30))
print(progress_bar(50, 30))
print(progress_bar(75, 30))
print(progress_bar(100, 30))
```
