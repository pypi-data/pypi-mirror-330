# Complex Styling Examples

This document provides examples of more complex styling operations using the charstyle library.

## Styling Text with Delimiters

The `styled_split` function allows you to split text by a delimiter and apply different styles to each part.

```python
from charstyle import styled, Style, styled_split

# Split text by a delimiter and apply different styles to each part
text = "Status: OK"
result = styled_split(text, ":", Style.RED, Style.GREEN)
print(result)  # "Status" in red and " OK" in green

# With multiple delimiters
text = "First:Second:Third"
result = styled_split(text, ":", Style.RED, Style.GREEN, Style.BLUE)
print(result)  # "First" in red, "Second" in green, and "Third" in blue

# With multiple styles per part
text = "Error: File not found"
result = styled_split(text, ":", (Style.BOLD, Style.RED), (Style.ITALIC, Style.YELLOW))
print(result)  # "Error" in bold red and " File not found" in italic yellow
```

## Styling Text with Regular Expressions

The `styled_pattern` function allows you to style text based on regular expression patterns.

```python
from charstyle import styled, Style, styled_pattern

# Style text that matches a pattern
text = "Hello World"
result = styled_pattern(text, r"(World)", Style.RED)
print(result)  # "Hello " unchanged and "World" in red

# Style multiple parts of text
text = "User: admin, Role: admin"
result = styled_pattern(text, r"(User|Role):(.*?)(,|$)", Style.BLUE, Style.GREEN)
print(result)  # "User" and "Role" in blue, and " admin" and " admin" in green

# Style a log message
text = "2023-04-15 [INFO] User logged in"
pattern = r"(\d{4}-\d{2}-\d{2})|(\[\w+\])|(.*)"
result = styled_pattern(text, pattern, Style.BLUE, Style.YELLOW, Style.WHITE)
print(result)  # Date in blue, log level in yellow, and message in white
```

## Styling Text with Named Patterns

The `styled_pattern_match` function allows you to style text based on named groups in a regular expression pattern.

```python
from charstyle import styled, Style, styled_pattern_match

# Style text with named groups
pattern = r"(?P<name>\w+): (?P<value>\d+)"
style_map = {"name": Style.RED, "value": Style.GREEN}
text = "Count: 42"
result = styled_pattern_match(text, pattern, style_map)
print(result)  # "Count" in red and "42" in green

# Style a log message
pattern = r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<level>\[\w+\]) (?P<message>.*)"
style_map = {
    "date": Style.BLUE,
    "level": Style.YELLOW,
    "message": Style.WHITE
}
text = "2023-04-15 [INFO] User logged in"
result = styled_pattern_match(text, pattern, style_map)
print(result)  # Date in blue, log level in yellow, and message in white

# Style a JSON-like string
pattern = r'"(?P<key>\w+)": "(?P<value>[^"]+)"'
style_map = {
    "key": (Style.BOLD, Style.BLUE),
    "value": Style.GREEN
}
text = '{"name": "John", "age": "30"}'
result = styled_pattern_match(text, pattern, style_map)
print(result)  # Keys in bold blue and values in green
```

## Formatting Styled Text

The `styled_format` function allows you to format text with styled values.

```python
from charstyle import styled, Style, styled_format

# Format text with styled values
result = styled_format("{} {}", ("Hello", Style.RED), ("World", Style.GREEN))
print(result)  # "Hello" in red and "World" in green

# Format text with named placeholders
result = styled_format("{name} is {age} years old",
                      name=("John", Style.BLUE),
                      age=("30", Style.GREEN))
print(result)  # "John" in blue and "30" in green

# Format text with mixed placeholders
result = styled_format("{} has {color} eyes",
                      ("Alice", Style.BOLD),
                      color=("blue", Style.BLUE))
print(result)  # "Alice" in bold and "blue" in blue
```

## Combining Multiple Styling Functions

You can combine multiple styling functions to create complex styled text.

```python
from charstyle import styled, Style, styled_split, styled_format

# Combine styled_split and styled_format
name = "John Doe"
age = 30
text = styled_format("{}: {}",
                    ("Name", (Style.BOLD, Style.BLUE)),
                    (name, Style.GREEN))
text += "\n" + styled_format("{}: {}",
                           ("Age", (Style.BOLD, Style.BLUE)),
                           (str(age), Style.GREEN))
print(text)  # "Name" in bold blue, "John Doe" in green, "Age" in bold blue, and "30" in green

# Combine styled_split and styled
header = styled("User Information", (Style.BOLD, Style.UNDERLINE))
details = styled_split("Email: john@example.com", ":",
                      (Style.BOLD, Style.BLUE),
                      Style.GREEN)
print(f"{header}\n{details}")  # Header in bold and underlined, "Email" in bold blue, and "john@example.com" in green
