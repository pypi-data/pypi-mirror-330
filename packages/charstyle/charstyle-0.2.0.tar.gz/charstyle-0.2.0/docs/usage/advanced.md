# Advanced Usage

This page covers advanced usage of charstyle for complex text styling.

## Creating Reusable Styles

```python
from charstyle import styled, Style

# Create reusable style tuples
error_style = (Style.RED, Style.BOLD)
warning_style = (Style.YELLOW, Style.ITALIC)
success_style = (Style.GREEN,)

# Apply styles to text
print(styled("Error: Operation failed", error_style))
print(styled("Warning: This operation might take a while", warning_style))
print(styled("Success: Operation completed", success_style))
```

## Styling Parts of Text

### Using styled_split

Split a string by a delimiter and apply different styles to each part:

```python
from charstyle import styled, Style, styled_split

# Style a key-value pair with different styles
print(styled_split("Status: OK", ":", Style.BOLD, Style.GREEN))
print(styled_split("Error: File not found", ":", (Style.RED, Style.BOLD), Style.RED))

# For multiple delimiters, make sure the number of styles matches the number of parts
print(styled_split("a,b,c", ",", Style.RED, Style.GREEN, Style.BLUE))

# This would raise a ValueError because there are 3 parts but only 2 styles
# print(styled_split("a,b,c", ",", Style.RED, Style.GREEN))
```

Note: The number of styles must match the number of parts after splitting the text by the delimiter. If there's a mismatch, a `ValueError` will be raised.

### Using styled_pattern

Style different parts of a string based on a regular expression pattern:

```python
from charstyle import styled, Style, styled_pattern

# Style a log message with timestamp and level
log_message = "2023-05-15 10:30:45 [INFO] User logged in"
pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (.*)"

# Style each captured group
print(styled_pattern(log_message, pattern, Style.BLUE, Style.YELLOW, Style.GREEN))
```

### Using styled_pattern_match

Style different parts of a string based on named capture groups in a regular expression:

```python
from charstyle import styled, Style, styled_pattern_match

# Log entry styling
pattern = r"(?P<timestamp>\d{2}:\d{2}:\d{2}) (?P<level>\w+): (?P<message>.*)"
styles = {
    "timestamp": Style.BRIGHT_BLACK,
    "level": (Style.GREEN, Style.BOLD),
    "message": Style.WHITE,
}

styled_text = styled_pattern_match(
    "14:25:36 INFO: User authentication successful",
    pattern,
    styles
)
print(styled_text)
```

### Using styled_format

Format a string with styled values:

```python
from charstyle import styled, Style, styled_format

# Format with positional arguments
print(
    styled_format(
        "{} = {}",
        ("username", Style.BLUE),
        ("admin", Style.GREEN)
    )
)
```

## Combining Different Techniques

You can combine different styling techniques for more complex output:

```python
from charstyle import styled, Style, styled_pattern_match

# Style a log message with named groups
log_message = "2023-05-15 10:30:45 [INFO] User logged in successfully from 192.168.1.1"
pattern = r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(?P<level>\w+)\] (?P<message>.*) from (?P<ip>\d+\.\d+\.\d+\.\d+)"

styles = {
    "timestamp": Style.BRIGHT_BLACK,
    "level": (Style.GREEN, Style.BOLD),
    "message": Style.WHITE,
    "ip": (Style.CYAN, Style.ITALIC)
}

styled_log = styled_pattern_match(log_message, pattern, styles)
print(styled_log)
```

## Practical Examples

### Log Message Styling

```python
from charstyle import styled, Style, styled_pattern_match

# Sample log message
log_message = "2023-04-15 12:34:56 [ERROR] Failed to connect to database: Connection refused"

# Define a pattern to match log components
pattern = r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(?P<level>\w+)\] (?P<message>.*)"

# Define styles for each component
styles = {
    "timestamp": Style.BLUE,
    "level": (Style.RED, Style.BOLD),
    "message": Style.WHITE
}

# Apply styling
styled_log = styled_pattern_match(log_message, pattern, styles)
print(styled_log)
```

### Configuration File Styling

```python
from charstyle import styled, Style, styled_pattern

# Sample configuration line
config_line = "database.host = localhost # Primary database server"

# Style different parts of the configuration
styled_config = styled_pattern(
    config_line,
    r"(\.)|( = )|(#.*)",
    (Style.BLUE, Style.BOLD),  # "database"
    Style.CYAN,              # "host"
    Style.GREEN,             # "localhost"
    (Style.YELLOW, Style.ITALIC)  # "# Primary database server"
)
print(styled_config)
```

### Command Output Styling

```python
from charstyle import styled, Style, styled_split, styled_pattern

# Sample command output
command_output = "Total: 42 files, 156 directories, 8.5 MB"

# Style using split
print(styled_split(command_output, ":", (Style.BOLD, Style.BLUE), Style.GREEN))

# Style using pattern
print(
    styled_pattern(
        command_output,
        r"(\d+)|(\d+\.\d+)",
        Style.WHITE,  # "Total"
        Style.YELLOW, # "42"
        Style.WHITE,  # " files, "
        Style.YELLOW, # "156"
        Style.WHITE,  # " directories, "
        Style.YELLOW, # "8.5"
        Style.WHITE   # " MB"
    )
)
```

### Command Output Styling

Style the output of a command to highlight important information:

```python
from charstyle import styled, Style, styled_split, styled_pattern

# Sample command output
command_output = "Status: Running\nUptime: 3d 4h 12m\nCPU: 45%\nMemory: 1.2GB/8GB"

# Style each line differently
for line in command_output.split("\n"):
    print(styled_split(line, ":", (Style.BOLD, Style.BLUE), Style.GREEN))
```

## See Also

- [Basic Usage](basic.md) - Introduction to basic styling
- [Styling Options](styling-options.md) - All available styles and colors
- [API Reference](../api/complex-styling.md) - Detailed API documentation for complex styling functions
