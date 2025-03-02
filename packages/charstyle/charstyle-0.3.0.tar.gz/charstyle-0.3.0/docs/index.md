# charstyle Documentation

Welcome to the documentation for **charstyle**, a Python library for styling terminal text output using ANSI escape sequences.

## Overview

charstyle provides a simple and intuitive API for adding color, background color, and text styles (bold, italic, underline, etc.) to text output in terminal applications.

```python
from charstyle import styled, Style

# Simple styling
print(styled("This is red and bold text", (Style.RED, Style.BOLD)))

# With alignment
from charstyle import Align
print(styled("Centered Title", Style.BOLD, width=40, align=Align.CENTER, fill_char="="))
```

## Features

- **Simple API**: Easy-to-use functions for styling text
- **Enum-based Constants**: Type-safe constants for colors and styles
- **Style Tuples**: Combine multiple styles in a single parameter
- **Text Alignment**: Left, right, and center alignment with custom fill characters
- **Pattern Styling**: Advanced functions for styling parts of strings
- **Terminal Icons**: Built-in icons for terminal output

## Installation

```bash
pip install charstyle
```

## Quick Links

- [Getting Started](getting-started.md): Quick introduction to charstyle
- [Basic Usage](usage/basic.md): Learn the basics of styling text
- [Text Alignment](usage/alignment.md): Learn about alignment and formatting features
- [Advanced Usage](usage/advanced.md): Explore complex styling techniques
- [API Reference](api/core.md): Detailed documentation of the API
