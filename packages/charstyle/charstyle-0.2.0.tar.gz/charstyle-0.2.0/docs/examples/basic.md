# Basic Examples

This page provides basic examples of using charstyle for styling terminal text.

## Basic Text Coloring

```python
from charstyle import RED, GREEN, BLUE, YELLOW, MAGENTA, CYAN, colored

# Color text
print(colored("This text is red", color=RED))
print(colored("This text is green", color=GREEN))
print(colored("This text is blue", color=BLUE))
print(colored("This text is yellow", color=YELLOW))
print(colored("This text is magenta", color=MAGENTA))
print(colored("This text is cyan", color=CYAN))
```

Output:
```
This text is red
This text is green
This text is blue
This text is yellow
This text is magenta
This text is cyan
```

## Text Styles

```python
from charstyle import BOLD, ITALIC, UNDERLINE, STRIKE, DIM, colored

# Apply text styles
print(colored("This text is bold", style=BOLD))
print(colored("This text is italic", style=ITALIC))
print(colored("This text is underlined", style=UNDERLINE))
print(colored("This text is strikethrough", style=STRIKE))
print(colored("This text is dimmed", style=DIM))
```

Output:
```
This text is bold
This text is italic
This text is underlined
This text is strikethrough
This text is dimmed
```

## Background Colors

```python
from charstyle import BG_RED, BG_GREEN, BG_BLUE, BG_YELLOW, BG_MAGENTA, BG_CYAN, colored

# Apply background colors
print(colored("Text with red background", bg_color=BG_RED))
print(colored("Text with green background", bg_color=BG_GREEN))
print(colored("Text with blue background", bg_color=BG_BLUE))
print(colored("Text with yellow background", bg_color=BG_YELLOW))
print(colored("Text with magenta background", bg_color=BG_MAGENTA))
print(colored("Text with cyan background", bg_color=BG_CYAN))
```

Output:
```
Text with red background
Text with green background
Text with blue background
Text with yellow background
Text with magenta background
Text with cyan background
```

## Combining Styles

```python
from charstyle import RED, GREEN, BLUE, BG_YELLOW, BG_RED, BG_BLUE, BOLD, UNDERLINE, ITALIC, colored

# Combine color and style
print(colored("Bold red text", color=RED, style=BOLD))
print(colored("Underlined green text", color=GREEN, style=UNDERLINE))
print(colored("Italic blue text", color=BLUE, style=ITALIC))

# Combine color, background, and style
print(colored("Bold red text on yellow background", color=RED, bg_color=BG_YELLOW, style=BOLD))
print(colored("Underlined white text on red background", bg_color=BG_RED, style=UNDERLINE))
print(colored("Bold italic text on blue background", bg_color=BG_BLUE, style=(BOLD, ITALIC)))
```

Output:
```
Bold red text
Underlined green text
Italic blue text
Bold red text on yellow background
Underlined white text on red background
Bold italic text on blue background
```

## Convenience Functions

```python
from charstyle import red, green, blue, yellow, bold, italic, underline
from charstyle import BOLD, ITALIC, UNDERLINE

# Use convenience functions
print(red("This text is red"))
print(green("This text is green"))
print(blue("This text is blue"))
print(yellow("This text is yellow"))

# Combine convenience functions
print(bold(red("This text is bold and red")))
print(italic(green("This text is italic and green")))
print(underline(blue("This text is underlined and blue")))

# Add style parameter to convenience functions
print(red("This text is red and bold", style=BOLD))
print(green("This text is green and italic", style=ITALIC))
print(blue("This text is blue and underlined", style=UNDERLINE))
```

Output:
```
This text is red
This text is green
This text is blue
This text is yellow
This text is bold and red
This text is italic and green
This text is underlined and blue
This text is red and bold
This text is green and italic
This text is blue and underlined
```

## Creating Reusable Styles

```python
from charstyle import RED, YELLOW, GREEN, BOLD, ITALIC, Style

# Create reusable styles
error_style = Style(color=RED, style=BOLD)
warning_style = Style(color=YELLOW, style=ITALIC)
success_style = Style(color=GREEN, style=BOLD)

# Apply styles to text
print(error_style("Error: Operation failed"))
print(warning_style("Warning: This operation might take a while"))
print(success_style("Success: Operation completed"))

# Reuse the same styles for different messages
print(error_style("Error: Connection refused"))
print(warning_style("Warning: Low disk space"))
print(success_style("Success: Data saved"))
```

Output:
```
Error: Operation failed
Warning: This operation might take a while
Success: Operation completed
Error: Connection refused
Warning: Low disk space
Success: Data saved
```

## Simple Logging Example

```python
from charstyle import RED, YELLOW, GREEN, BLUE, BOLD, colored
import time

def log(level, message):
    timestamp = time.strftime("%H:%M:%S")

    if level == "ERROR":
        level_styled = colored(level, color=RED, style=BOLD)
    elif level == "WARNING":
        level_styled = colored(level, color=YELLOW, style=BOLD)
    elif level == "INFO":
        level_styled = colored(level, color=GREEN)
    elif level == "DEBUG":
        level_styled = colored(level, color=BLUE)
    else:
        level_styled = level

    print(f"[{timestamp}] {level_styled}: {message}")

# Example usage
log("INFO", "Application started")
log("DEBUG", "Loading configuration")
log("WARNING", "Configuration file not found, using defaults")
log("ERROR", "Failed to connect to database")
log("INFO", "Retrying connection in 5 seconds")
```

Output:
```
[21:45:30] INFO: Application started
[21:45:30] DEBUG: Loading configuration
[21:45:30] WARNING: Configuration file not found, using defaults
[21:45:30] ERROR: Failed to connect to database
[21:45:30] INFO: Retrying connection in 5 seconds
