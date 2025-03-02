# charstyle

[![PyPI version](https://badge.fury.io/py/charstyle.svg)](https://badge.fury.io/py/charstyle)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/charstyle.svg)](https://pypi.org/project/charstyle/)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://joaompinto.github.io/charstyle/)

A simple Python library for styling terminal text output using ANSI escape sequences.

## Features

- Text colors (normal and bright variants)
- Background colors (normal and bright variants)
- Text styles (bold, italic, underline, etc.)
- Chainable style combinations
- Custom style definitions
- Complex string styling with multiple components
- Terminal icons/emojis that work in most modern terminals
- Windows 10+ compatibility

## Installation

**Requirements:** Python 3.11 or higher

```bash
pip install charstyle
```

For development and contributing to the project, see [README_DEVELOP.md](README_DEVELOP.md).

## Usage

### Basic Usage

```python
# Import the styled function and Style
from charstyle import styled, Style

# Apply basic styles
print(styled("This is red text", Style.RED))
print(styled("This is blue text", Style.BLUE))
print(styled("This is bold text", Style.BOLD))
print(styled("This is underlined text", Style.UNDERLINE))

# Combining styles with tuples
print(styled("Red text with underline", (Style.RED, Style.UNDERLINE)))
print(styled("Bold blue text", (Style.BLUE, Style.BOLD)))
```

### Using Style Tuples

```python
# Import styled function and Style
from charstyle import styled, Style

# Apply styles with Style enum values
print(styled("Red text", Style.RED))
print(styled("Blue text", Style.BLUE))
print(styled("Bold text", Style.BOLD))
print(styled("Underlined text", Style.UNDERLINE))

# Mix styles with tuples
print(styled("Bold yellow text", (Style.YELLOW, Style.BOLD)))
print(styled("Underlined red text", (Style.RED, Style.UNDERLINE)))

# Custom color and background
print(styled("Custom color and background", (Style.RED, Style.BG_BLUE, Style.BOLD)))
```

### Alignment and Width Formatting

```python
# Import the Align enum for text alignment
from charstyle import styled, Style, Align

# Fixed width examples
print(styled("Default left align", Style.GREEN, width=30))
print(styled("Right aligned", Style.YELLOW, width=30, align=Align.RIGHT))
print(styled("Center aligned", Style.CYAN, width=30, align=Align.CENTER))

# Custom fill character examples
print(styled("Header", Style.BOLD, width=20, fill_char="-", align=Align.CENTER))
print(styled("Title", Style.UNDERLINE, width=40, fill_char="=", align=Align.CENTER))

# Table-like formatting
headers = [
    styled("ID", Style.BOLD, width=5, align=Align.CENTER),
    styled("Name", Style.BOLD, width=20, align=Align.CENTER),
    styled("Status", Style.BOLD, width=15, align=Align.CENTER),
]
print("".join(headers))
```

### Creating Tables

```python
from charstyle import tabled, Style, Align

# Sample data
headers = ["ID", "Name", "Department", "Status"]
rows = [
    ["1", "Alice Smith", "Engineering", "Active"],
    ["2", "Bob Johnson", "Marketing", "Inactive"],
    ["3", "Carol Williams", "Finance", "Active"],
]

# Simple table
print(tabled(headers, rows))

# Styled table with borders (default style)
print(tabled(
    headers,
    rows,
    header_style=Style.BOLD,
    widths=[5, 20, 15, 12],
    alignments=[Align.CENTER, Align.LEFT, Align.LEFT, Align.CENTER],
    borders=True
))

# Compact style table
print(tabled(
    headers,
    rows,
    style="compact",
    header_style=Style.UNDERLINE
))

# Thin style table
print(tabled(
    headers,
    rows,
    style="thin",
    header_style=(Style.BOLD, Style.UNDERLINE)
))

# Table with conditional formatting
def status_formatter(row, col, value):
    if col == 3:  # Status column
        if value == "Active":
            return styled(value, Style.GREEN, align=Align.CENTER)
        else:
            return styled(value, Style.RED, align=Align.CENTER)
    return None

print(tabled(
    headers,
    rows,
    header_style=Style.BOLD,
    cell_formatter=status_formatter,
    borders=True
))
```

### Advanced Usage

```python
from charstyle import styled, Style

# Combine foreground color, background color, and style
print(styled("Custom styling", (Style.YELLOW, Style.BG_BLUE, Style.BOLD)))

# Create predefined styles as tuples
error_style = (Style.BRIGHT_RED, Style.BOLD)
warning_style = (Style.YELLOW, Style.ITALIC)
success_style = (Style.GREEN,)

# Apply error style
error_message = "Error: Something went wrong!"
print(styled(error_message, error_style))

# Apply warning style
print(styled("Warning: This is a warning message", warning_style))
```

### Combining Multiple Styles

```python
from charstyle import styled, Style

# Method 1: Using the style parameter with a tuple of styles
print(styled("Bold and Italic",
              (Style.BOLD, Style.ITALIC)))

# Method 2: Using predefined style tuples
bold_italic = (Style.BOLD, Style.ITALIC)
print(styled("Bold and Italic (Style class)", bold_italic))

# Method 3: Combining styles with colors
print(styled("Bold red italic",
              (Style.RED, Style.BOLD, Style.ITALIC)))

# Fancy style with multiple attributes
fancy_style = (Style.BRIGHT_GREEN, Style.BG_BLACK, Style.BOLD, Style.UNDERLINE)
print(styled("Bold underlined bright green text on black background", fancy_style))
```

### CLI Commands

charstyle includes a command-line interface for exploring available styles, icons, and table formatting options:

```bash
# Display a summary of available commands
python -m charstyle

# Display all available text styles
python -m charstyle styles

# Display all available icons
python -m charstyle icons

# Display icons from a specific category
python -m charstyle icons Hearts

# Display all table formatting examples
python -m charstyle tables

# Display a specific table style (default, compact, or thin)
python -m charstyle tables default
python -m charstyle tables compact
python -m charstyle tables thin
```

### Complex Styling Functions

For more advanced styling needs, charstyle provides several complex styling functions:

```python
from charstyle import (
    styled_split, styled_pattern, styled_pattern_match, styled_format,
    Style
)

# Style different parts of a string split by a delimiter
status = styled_split("Status: Online", ":", Style.BOLD, Style.GREEN)
# "Status" in bold, "Online" in green

# Style text by matching a regex pattern
text = "The value is 42 and the status is active"
styled = styled_pattern(text, r"(value is \d+)|(status is \w+)",
                      Style.RED, Style.GREEN)
# "value is 42" in red, "status is active" in green

# Style text using named regex groups
log = "2023-04-15 [INFO] User logged in"
styled_log = styled_pattern_match(
    log,
    r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<level>\[\w+\]) (?P<msg>.*)",
    {"date": Style.BLUE, "level": Style.GREEN, "msg": Style.YELLOW}
)

# Format-style placeholders with styles
from charstyle import styled_format, Style
template = "User {name} logged in from {ip}"
formatted = styled_format(template,
                        name=("admin", Style.GREEN),
                        ip=("192.168.1.100", Style.RED))
```

### Terminal Icons

charstyle includes a collection of widely supported terminal icons that display correctly in most modern terminals:

```python
from charstyle import Icon, styled, Style

# Use individual icons
print(f"{Icon.CHECK} {styled('Task completed', Style.BOLD)}")
print(f"{Icon.CROSS} {styled('Task failed', Style.RED)}")
print(f"{Icon.WARNING} {styled('Warning message', Style.ITALIC)}")

# Create a simple box
print(f"{Icon.TOP_LEFT}{Icon.H_LINE * 10}{Icon.TOP_RIGHT}")
print(f"{Icon.V_LINE}{' ' * 10}{Icon.V_LINE}")
print(f"{Icon.BOTTOM_LEFT}{Icon.H_LINE * 10}{Icon.BOTTOM_RIGHT}")
```

View all available icons:

```bash
python -m charstyle --icons
```

## Available Styles

### Text Styles
- Style.BOLD
- Style.DIM
- Style.ITALIC
- Style.UNDERLINE
- Style.BLINK
- Style.REVERSE
- Style.HIDDEN
- Style.STRIKETHROUGH

### Foreground Colors
- Style.BLACK
- Style.RED
- Style.GREEN
- Style.YELLOW
- Style.BLUE
- Style.MAGENTA
- Style.CYAN
- Style.WHITE
- Style.BRIGHT_BLACK
- Style.BRIGHT_RED
- Style.BRIGHT_GREEN
- Style.BRIGHT_YELLOW
- Style.BRIGHT_BLUE
- Style.BRIGHT_MAGENTA
- Style.BRIGHT_CYAN
- Style.BRIGHT_WHITE

### Background Colors
- Style.BG_BLACK
- Style.BG_RED
- Style.BG_GREEN
- Style.BG_YELLOW
- Style.BG_BLUE
- Style.BG_MAGENTA
- Style.BG_CYAN
- Style.BG_WHITE
- Style.BG_BRIGHT_BLACK
- Style.BG_BRIGHT_RED
- Style.BG_BRIGHT_GREEN
- Style.BG_BRIGHT_YELLOW
- Style.BG_BRIGHT_BLUE
- Style.BG_BRIGHT_MAGENTA
- Style.BG_BRIGHT_CYAN
- Style.BG_BRIGHT_WHITE

## Author

- **João Pinto** - [joaompinto](https://github.com/joaompinto)

## Development

For developers who want to contribute to this project, please see:

- [CONTRIBUTING.md](CONTRIBUTING.md) - Guidelines for contributing to the project
- [README_DEVELOP.md](README_DEVELOP.md) - Detailed guide for development workflows

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Documentation

For more detailed documentation, visit our [GitHub Pages documentation site](https://joaompinto.github.io/charstyle/).

The documentation includes:
- Detailed usage guides
- API reference
- Examples and tutorials
- Contributing guidelines
