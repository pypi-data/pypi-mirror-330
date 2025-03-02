# Complex Styling API

This page documents the complex styling functions available in charstyle.

## styled_split

Split a string by a delimiter and apply different styles to each part.

```python
styled_split(text: str, delimiter: str, *styles: StyleType) -> str
```

**Parameters:**
- `text` (str): The text to style
- `delimiter` (str): The delimiter to split the text by
- `*styles` (StyleType): The styles to apply to each part

**Returns:**
- `str`: The styled text

**Raises:**
- `ValueError`: If the number of parts after splitting doesn't match the number of styles

**Example:**
```python
from charstyle import styled, Style, styled_split

# Style a key-value pair with different styles
print(styled_split("Status: Success", ":", Style.BOLD, Style.GREEN))
print(styled_split("Error: File not found", ":", (Style.RED, Style.BOLD), Style.RED))

# This would raise a ValueError because there are 3 parts but only 2 styles
# print(styled_split("a,b,c", ",", Style.RED, Style.GREEN))
```

## styled_pattern

Style different parts of a string based on a regular expression pattern.

```python
styled_pattern(text: str, pattern: str, *styles: StyleType) -> str
```

**Parameters:**
- `text` (str): The text to style
- `pattern` (str): The regular expression pattern to split the text by
- `*styles` (StyleType): The styles to apply to each part

**Returns:**
- `str`: The styled text

**Example:**
```python
from charstyle import styled, Style, styled_pattern

# Style with regular expression pattern
print(
    styled_pattern(
        "Status: OK (processed)",
        r"(: |\()",
        Style.BLUE,   # "Status"
        Style.GREEN,  # "OK "
        Style.YELLOW, # "processed)"
    )
)
```

## styled_pattern_match

Style different parts of a string based on named capture groups in a regular expression.

```python
styled_pattern_match(text: str, pattern: str, styles: Dict[str, StyleType]) -> str
```

**Parameters:**
- `text` (str): The text to style
- `pattern` (str): The regular expression pattern with named capture groups
- `styles` (Dict[str, StyleType]): A dictionary mapping group names to styles

**Returns:**
- `str`: The styled text

**Example:**
```python
from charstyle import styled, Style, styled_pattern_match

pattern = r"(?P<code>\d{3}) (?P<status>\w+) - (?P<message>.*)"
text = "404 Not Found - The requested resource was not found"

styled_text = styled_pattern_match(
    text,
    pattern,
    {
        "code": Style.RED,
        "status": (Style.YELLOW, Style.BOLD),
        "message": Style.BLUE
    }
)
print(styled_text)
```

## styled_format

Style different parts of a string using a format string with placeholders.

```python
styled_format(template: str, **kwargs: Tuple[str, StyleType]) -> str
```

**Parameters:**
- `template` (str): A format string with placeholders
- `**kwargs`: Keyword arguments where each value is a tuple of (text, style)

**Returns:**
- `str`: The styled text

**Example:**
```python
from charstyle import styled, Style, styled_format

# Style with format placeholders
print(
    styled_format(
        "User {username} logged in from {ip}",
        username=("admin", Style.GREEN),
        ip=("192.168.1.1", Style.RED)
    )
)
