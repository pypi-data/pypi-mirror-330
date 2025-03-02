# Getting Started with charstyle

This guide will help you get started with charstyle, a Python library for styling terminal text.

## Installation

Install charstyle using pip:

```bash
pip install charstyle
```

## Basic Usage

Here's a simple example to get you started:

```python
from charstyle import styled, Style

# Basic color
print(styled("This is red text", Style.RED))

# Color with style
print(styled("This is bold blue text", (Style.BLUE, Style.BOLD)))

# Multiple styles
print(styled("This is bold green text on yellow background",
             (Style.GREEN, Style.BOLD, Style.BG_YELLOW)))

# Text alignment
from charstyle import Align
print(styled("Centered Header", Style.BOLD, width=30, align=Align.CENTER))
print(styled("Right aligned", Style.YELLOW, width=30, align=Align.RIGHT))
```

## Development Setup

If you want to contribute to charstyle or modify it for your own needs:

1. Install Hatch:
   ```bash
   pip install hatch
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/joaompinto/charstyle.git
   cd charstyle
   ```

3. Run tests to verify everything is working:
   ```bash
   hatch -e dev run test
   ```

For more detailed development instructions, see the [Contributing Guide](contributing.md).

## Next Steps

Now that you have charstyle installed and know the basics, you can:

1. Learn more about [basic usage](usage/basic.md)
2. Explore [text alignment features](usage/alignment.md)
3. Explore [advanced styling techniques](usage/advanced.md)
4. Check out the [API reference](api/core.md)

## Example: Styled Output

Here's a more complete example showing how to create styled terminal output:

```python
from charstyle import styled, Style, Align

# Define some reusable styles
header_style = (Style.BLUE, Style.BOLD)
success_style = (Style.GREEN, Style.BOLD)
error_style = (Style.RED, Style.BOLD)
warning_style = (Style.YELLOW, Style.ITALIC)

# Create a header with alignment
print(styled("APPLICATION STATUS", header_style, width=50, align=Align.CENTER, fill_char="="))

# Use the styles
print(styled("✓ Database connection: ", success_style) + "Connected")
print(styled("✓ Configuration: ", success_style) + "Loaded")
print(styled("⚠ Disk space: ", warning_style) + "Running low")
print(styled("✗ External API: ", error_style) + "Unavailable")
```

## Requirements

- Python 3.11 or higher
- A terminal that supports ANSI color codes
