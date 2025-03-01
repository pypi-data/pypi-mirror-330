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
```

## Next Steps

Now that you have charstyle installed and know the basics, you can:

1. Learn more about [basic usage](usage/basic.md)
2. Explore [advanced styling techniques](usage/advanced.md)
3. Check out the [API reference](api/core.md)

## Example: Styled Output

Here's a more complete example showing how to create styled terminal output:

```python
from charstyle import styled, Style

# Define some reusable styles
header_style = (Style.BLUE, Style.BOLD)
success_style = (Style.GREEN, Style.BOLD)
error_style = (Style.RED, Style.BOLD)
warning_style = (Style.YELLOW, Style.ITALIC)

# Use the styles
print(styled("APPLICATION STATUS", header_style))
print(styled("✓ Database connection: ", success_style) + "Connected")
print(styled("✓ Configuration: ", success_style) + "Loaded")
print(styled("⚠ Disk space: ", warning_style) + "Running low")
print(styled("✗ External API: ", error_style) + "Unavailable")
```

## Requirements

- Python 3.11 or higher
- A terminal that supports ANSI color codes
