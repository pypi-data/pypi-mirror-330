# Style Tuples API

This page documents how to use style tuples in the charstyle library.

## Style Tuples

Style tuples allow you to create reusable style combinations by grouping multiple style enum values.

### Creating Style Tuples

```python
# Basic syntax
style_tuple = (Style.RED, Style.BOLD)
```

**Components:**

- Style enum values from the `Style` enum
- Can include foreground colors, background colors, and text styles in any combination

## Available Styles

For a complete list of all available style enum values that can be used in style tuples, see the [Styling Options](../usage/styling-options.md#available-styles) documentation.

### Usage

```python
from charstyle import styled, Style

# Create a style tuple
error_style = (Style.RED, Style.BG_BLACK, Style.BOLD)

# Apply the style to text
styled_text = styled("Error message", error_style)
print(styled_text)
```

## Common Style Tuple Patterns

### Color + Style

```python
from charstyle import styled, Style

# Combine a color with a text style
warning_style = (Style.YELLOW, Style.BOLD)
print(styled("Warning: Low disk space", warning_style))
```

### Color + Background

```python
from charstyle import styled, Style

# Combine foreground and background colors
highlight_style = (Style.BLACK, Style.BG_YELLOW)
print(styled("IMPORTANT", highlight_style))
```

### Multiple Text Styles

```python
from charstyle import styled, Style

# Combine multiple text styles
emphasis_style = (Style.BOLD, Style.UNDERLINE)
print(styled("Critical Information", emphasis_style))
```

### Complex Combinations

```python
from charstyle import styled, Style

# Combine multiple types of styles
fancy_style = (Style.BRIGHT_RED, Style.BG_BLACK, Style.BOLD, Style.UNDERLINE)
print(styled("URGENT: Action Required", fancy_style))
```

## Style Tuples vs. Direct Styling

You can either create reusable style tuples or apply styles directly:

```python
from charstyle import styled, Style

# Method 1: Reusable style tuple
error_style = (Style.RED, Style.BOLD)
print(styled("Error: Connection failed", error_style))

# Method 2: Direct styling
print(styled("Error: Connection failed", (Style.RED, Style.BOLD)))
```

## Best Practices

1. **Create named style tuples** for styles you use frequently
2. **Group related styles** into a set of consistent tuples
3. **Use descriptive names** that indicate the purpose of the style
4. **Keep style definitions centralized** in one part of your codebase

## See Also

- [Core API](core.md) - Documentation for the core styling functions
- [Complex Styling](complex-styling.md) - Advanced styling techniques
