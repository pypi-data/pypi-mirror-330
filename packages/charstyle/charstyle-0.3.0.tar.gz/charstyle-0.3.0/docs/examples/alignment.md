# Alignment Examples

This page provides examples of using the alignment and formatting features in charstyle.

## Basic Alignment

```python
from charstyle import styled, Style, Align

# Left alignment (default)
print(styled("Left aligned", Style.GREEN, width=30))

# Right alignment
print(styled("Right aligned", Style.YELLOW, width=30, align=Align.RIGHT))

# Center alignment
print(styled("Center aligned", Style.CYAN, width=30, align=Align.CENTER))
```

Output:
```
Left aligned
                  Right aligned
        Center aligned
```

## Custom Fill Characters

```python
from charstyle import styled, Style, Align

# Create a header with dashes
print(styled("Header", Style.BOLD, width=20, fill_char="-", align=Align.CENTER))

# Create a title with equals signs
print(styled("Title", Style.UNDERLINE, width=40, fill_char="=", align=Align.CENTER))

# Create a section divider
print(styled("", None, width=50, fill_char="*"))
```

Output:
```
-------Header-------
=================Title==================
**************************************************
```

## Creating a Simple Table

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

Output:
```
  ID         Name             Status
----------------------------------------
  1  Project Alpha            Active
  2  Project Beta            Pending
  3  Project Gamma            Failed
```

## Creating a Dashboard

```python
from charstyle import styled, Style, Align

# Main header
print(styled("SYSTEM DASHBOARD", Style.BOLD, width=60, fill_char="=", align=Align.CENTER))

# CPU section
print("\n" + styled("CPU", Style.BOLD, width=30, fill_char="-", align=Align.CENTER))
print(styled("Usage:", Style.BOLD, width=15) + styled("45%", Style.GREEN))
print(styled("Temperature:", Style.BOLD, width=15) + styled("65°C", Style.YELLOW))
print(styled("Cores:", Style.BOLD, width=15) + styled("8", Style.CYAN))

# Memory section
print("\n" + styled("MEMORY", Style.BOLD, width=30, fill_char="-", align=Align.CENTER))
print(styled("Usage:", Style.BOLD, width=15) + styled("3.2GB / 16GB", Style.GREEN))
print(styled("Available:", Style.BOLD, width=15) + styled("12.8GB", Style.CYAN))

# Storage section
print("\n" + styled("STORAGE", Style.BOLD, width=30, fill_char="-", align=Align.CENTER))
print(styled("Usage:", Style.BOLD, width=15) + styled("234GB / 512GB", Style.YELLOW))
print(styled("Available:", Style.BOLD, width=15) + styled("278GB", Style.CYAN))

# Footer
print("\n" + styled("Last updated: 2023-05-15 10:30:45", Style.DIM, width=60, align=Align.RIGHT))
```

This creates a nicely formatted dashboard with sections, aligned labels, and styled values.
