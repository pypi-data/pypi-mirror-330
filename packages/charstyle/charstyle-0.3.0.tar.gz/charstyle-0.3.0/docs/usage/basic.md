# Basic Usage

This guide covers the basic usage of charstyle for styling terminal text.

## Importing charstyle

```python
# Import the styled function and Style enum
from charstyle import styled, Style

# For alignment features, also import the Align enum
from charstyle import Align
```

## Foreground Colors

```python
from charstyle import styled, Style

# Apply colors to text
print(styled("This text is red", Style.RED))
print(styled("This text is green", Style.GREEN))
print(styled("This text is blue", Style.BLUE))
```

## Text Styles

```python
from charstyle import styled, Style

# Apply text styles
print(styled("This text is bold", Style.BOLD))
print(styled("This text is italic", Style.ITALIC))
print(styled("This text is underlined", Style.UNDERLINE))
print(styled("This text has strikethrough", Style.STRIKE))
```

## Background Colors

```python
from charstyle import styled, Style

# Apply background colors
print(styled("Red background", Style.BG_RED))
print(styled("Green background", Style.BG_GREEN))
print(styled("Blue background", Style.BG_BLUE))
```

## Combining Styles

You can combine multiple styles by passing a tuple of style constants:

```python
from charstyle import styled, Style

# Combine text style and foreground color
print(styled("Bold red text", (Style.RED, Style.BOLD)))
print(styled("Italic blue text", (Style.BLUE, Style.ITALIC)))

# Combine foreground and background colors
print(styled("Red text on blue background", (Style.RED, Style.BG_BLUE)))

# Combine text style, foreground color, and background color
print(styled("Bold green text on yellow background", (Style.GREEN, Style.BG_YELLOW, Style.BOLD)))
```

## Text Alignment

You can align text within a fixed width:

```python
from charstyle import styled, Style, Align

# Left alignment (default)
print(styled("Left aligned", Style.GREEN, width=30))

# Right alignment
print(styled("Right aligned", Style.YELLOW, width=30, align=Align.RIGHT))

# Center alignment
print(styled("Center aligned", Style.CYAN, width=30, align=Align.CENTER))

# Custom fill character
print(styled("Header", Style.BOLD, width=20, fill_char="-", align=Align.CENTER))
```

## Checking Terminal Support

charstyle includes a function to check if the current terminal supports colors:

```python
from charstyle import supports_color

if supports_color():
    print("Your terminal supports colors!")
else:
    print("Your terminal does not support colors.")
```

## Next Steps

Now that you've learned the basics, you can explore:

- [Text Alignment](alignment.md) - Learn about alignment and formatting features
- [Advanced Usage](advanced.md) - Learn about complex styling functions
- [Styling Options](styling-options.md) - See all available styles and colors
