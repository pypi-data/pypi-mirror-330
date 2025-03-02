# Styling Options

charstyle provides multiple ways to apply styles to your text. This guide explains when to use each approach.

## Style Constants

The most basic way to style text is using the built-in style enum values:

```python
from charstyle import styled, Style

# Using a color constant
print(styled("This is red text", Style.RED))

# Using a text style constant
print(styled("This is bold text", Style.BOLD))
```

## Combining Styles

When you need to apply multiple styles to the same text, you can use tuples of style enum values.

### Style Tuples

Style tuples allow you to combine multiple styles in a single parameter.

## When to Use Style Tuples

Style tuples provide a concise way to combine multiple styles.

### 1. When you need to combine color, background color, and text style

```python
from charstyle import styled, Style

# Combine foreground color, background color, and text style
print(styled("Warning", (Style.RED, Style.BG_BLACK, Style.BOLD)))

# Create a reusable style tuple
error_style = (Style.RED, Style.BOLD)
print(styled("Error: File not found", error_style))
```

### 2. When you need to apply multiple text styles

```python
from charstyle import styled, Style

# Combine multiple text styles
warning_style = (Style.YELLOW, Style.BOLD, Style.ITALIC)
print(styled("Warning: This operation is irreversible", warning_style))
```

### 3. When you need to create high-contrast combinations

```python
from charstyle import styled, Style

# Create high-contrast text
print(styled("CAUTION", (Style.BLACK, Style.BG_YELLOW)))
```

### 4. When you need complex styling combinations

```python
from charstyle import styled, Style

# Complex styling with multiple attributes
fancy_style = (Style.BRIGHT_GREEN, Style.BG_BLUE, Style.BOLD, Style.UNDERLINE)
print(styled("Success: Operation completed", fancy_style))
```

## Available Styles

charstyle provides a comprehensive set of styles through the `Style` enum. Here's a complete list of all available styles:

### Text Styles

| Style Name | Description |
|------------|-------------|
| `Style.NORMAL` | Reset all styles to normal |
| `Style.BOLD` | Bold text |
| `Style.DIM` | Dimmed text (reduced intensity) |
| `Style.ITALIC` | Italic text |
| `Style.UNDERLINE` | Underlined text |
| `Style.BLINK` | Blinking text (not supported in all terminals) |
| `Style.REVERSE` | Reverse video (swap foreground and background colors) |
| `Style.HIDDEN` | Hidden text (invisible) |
| `Style.STRIKE` | Strikethrough text |

### Foreground Colors

| Color Name | Description |
|------------|-------------|
| `Style.BLACK` | Black text |
| `Style.RED` | Red text |
| `Style.GREEN` | Green text |
| `Style.YELLOW` | Yellow text |
| `Style.BLUE` | Blue text |
| `Style.MAGENTA` | Magenta text |
| `Style.CYAN` | Cyan text |
| `Style.WHITE` | White text |
| `Style.DEFAULT` | Default text color |

### Bright Foreground Colors

| Color Name | Description |
|------------|-------------|
| `Style.BRIGHT_BLACK` | Bright black (gray) text |
| `Style.BRIGHT_RED` | Bright red text |
| `Style.BRIGHT_GREEN` | Bright green text |
| `Style.BRIGHT_YELLOW` | Bright yellow text |
| `Style.BRIGHT_BLUE` | Bright blue text |
| `Style.BRIGHT_MAGENTA` | Bright magenta text |
| `Style.BRIGHT_CYAN` | Bright cyan text |
| `Style.BRIGHT_WHITE` | Bright white text |

### Background Colors

| Color Name | Description |
|------------|-------------|
| `Style.BG_BLACK` | Black background |
| `Style.BG_RED` | Red background |
| `Style.BG_GREEN` | Green background |
| `Style.BG_YELLOW` | Yellow background |
| `Style.BG_BLUE` | Blue background |
| `Style.BG_MAGENTA` | Magenta background |
| `Style.BG_CYAN` | Cyan background |
| `Style.BG_WHITE` | White background |
| `Style.BG_DEFAULT` | Default background color |

### Bright Background Colors

| Color Name | Description |
|------------|-------------|
| `Style.BG_BRIGHT_BLACK` | Bright black (gray) background |
| `Style.BG_BRIGHT_RED` | Bright red background |
| `Style.BG_BRIGHT_GREEN` | Bright green background |
| `Style.BG_BRIGHT_YELLOW` | Bright yellow background |
| `Style.BG_BRIGHT_BLUE` | Bright blue background |
| `Style.BG_BRIGHT_MAGENTA` | Bright magenta background |
| `Style.BG_BRIGHT_CYAN` | Bright cyan background |
| `Style.BG_BRIGHT_WHITE` | Bright white background |

## Example: Using Different Style Categories

```python
from charstyle import styled, Style

# Text style + foreground color + background color
print(styled("Styled text", (Style.BOLD, Style.RED, Style.BG_YELLOW)))

# Bright foreground color
print(styled("Bright color", Style.BRIGHT_CYAN))

# Bright background color
print(styled("Bright background", Style.BG_BRIGHT_MAGENTA))

# Multiple text styles
print(styled("Bold and italic", (Style.BOLD, Style.ITALIC)))
```

## Styling Multiple Parts of Text

When you need to apply different styles to different parts of a string:

### 1. Using styled_split

```python
from charstyle import styled, Style, styled_split

# Split by delimiter and apply different styles
print(styled_split("Status: Active", ":", (Style.BOLD, Style.ITALIC), Style.GREEN))
```

### 2. Using styled_format

```python
from charstyle import styled, Style, styled_format

# Format with styled values
print(
    styled_format(
        "{} = {}",
        ("username", Style.BLUE),
        ("admin", Style.GREEN)
    )
)
```

### 3. Using styled_pattern

```python
from charstyle import styled, Style, styled_pattern

# Style using regex pattern
print(
    styled_pattern(
        "2023-05-15 10:30:45 [INFO] User logged in",
        r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (.*)",
        Style.BLUE,      # timestamp
        Style.YELLOW,    # log level
        Style.GREEN      # message
    )
)
```

### 4. Using styled_pattern_match

```python
from charstyle import styled, Style, styled_pattern_match

# Style using named regex groups
pattern = r"(?P<timestamp>\d{4}-\d{2}-\d{2}) (?P<level>\w+): (?P<message>.*)"
styles = {
    "timestamp": Style.BRIGHT_BLACK,
    "level": (Style.GREEN, Style.BOLD),
    "message": Style.WHITE
}
print(styled_pattern_match("2023-05-15 INFO: Operation successful", pattern, styles))
```

## Real-World Examples

### Error and Success Messages

```python
from charstyle import styled, Style, styled_split

# Function to create styled status messages
def status_message(status, message):
    status_line = styled_split("Database: Online", ":", (Style.BOLD, Style.WHITE), Style.GREEN)
    return status_line
```

## Best Practices

### 1. Create reusable style tuples for consistent styling

```python
from charstyle import styled, Style

# Define reusable styles
error_style = (Style.RED, Style.BOLD)
warning_style = (Style.YELLOW, Style.ITALIC)
success_style = (Style.GREEN, Style.BOLD)
info_style = (Style.BLUE, Style.ITALIC)

# Use them consistently throughout your application
print(styled("Error: Connection failed", error_style))
print(styled("Warning: Low disk space", warning_style))
```

### 2. Combine styling functions for complex output

```python
from charstyle import styled, Style, styled_split

# Combine different styling approaches
header = styled("SERVER STATUS", (Style.WHITE, Style.BG_BLUE, Style.BOLD))
status_line = styled_split("Database: Online", ":", (Style.BOLD, Style.WHITE), Style.GREEN)

print(f"{header}\n{status_line}")
```

## See Also

- [Basic Usage](basic.md) - Introduction to basic styling
- [Advanced Usage](advanced.md) - Complex styling techniques
- [API Reference](../api/core.md) - Detailed API documentation
