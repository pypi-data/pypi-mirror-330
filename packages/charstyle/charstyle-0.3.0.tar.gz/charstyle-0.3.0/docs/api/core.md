# Core API

This page documents the core API of charstyle.

## styled

Apply styles to text.

```python
styled(text: str, style: StyleType, width: int = None, align: Align = Align.LEFT, fill_char: str = " ") -> str
```

**Parameters:**
- `text` (str): The text to style
- `style` (StyleType): The style to apply. Can be a single style or a tuple of styles.
- `width` (int, optional): Fixed width for the output text. If specified, the text will be padded or truncated to this width.
- `align` (Align, optional): Alignment of the text within the fixed width. Default is `Align.LEFT`.
- `fill_char` (str, optional): Character used for filling the fixed width. Default is space.

**Returns:**
- `str`: The styled text

**Example:**
```python
from charstyle import styled, Style, Align

# Style with a single style
print(styled("Hello", Style.RED))

# Style with multiple styles
print(styled("Hello", (Style.BOLD, Style.RED)))
print(styled("Hello", (Style.BOLD, Style.UNDERLINE, Style.RED)))

# Style with background color
print(styled("Hello", (Style.RED, Style.BG_BLUE)))

# Style with fixed width and alignment
print(styled("Hello", Style.GREEN, width=20))
print(styled("Hello", Style.YELLOW, width=20, align=Align.RIGHT))
print(styled("Hello", Style.CYAN, width=20, align=Align.CENTER))

# Style with custom fill character
print(styled("Header", Style.BOLD, width=30, fill_char="-", align=Align.CENTER))
```

## Style

Enum containing all available styles.

```python
class Style(StrEnum):
    # Text styles
    NORMAL = "0"
    BOLD = "1"
    DIM = "2"
    ITALIC = "3"
    UNDERLINE = "4"
    BLINK = "5"
    REVERSE = "7"
    HIDDEN = "8"
    STRIKE = "9"

    # Foreground colors
    BLACK = "30"
    RED = "31"
    GREEN = "32"
    YELLOW = "33"
    BLUE = "34"
    MAGENTA = "35"
    CYAN = "36"
    WHITE = "37"
    DEFAULT = "39"

    # Bright foreground colors
    BRIGHT_BLACK = "90"
    BRIGHT_RED = "91"
    BRIGHT_GREEN = "92"
    BRIGHT_YELLOW = "93"
    BRIGHT_BLUE = "94"
    BRIGHT_MAGENTA = "95"
    BRIGHT_CYAN = "96"
    BRIGHT_WHITE = "97"

    # Background colors
    BG_BLACK = "40"
    BG_RED = "41"
    BG_GREEN = "42"
    BG_YELLOW = "43"
    BG_BLUE = "44"
    BG_MAGENTA = "45"
    BG_CYAN = "46"
    BG_WHITE = "47"
    BG_DEFAULT = "49"

    # Bright background colors
    BG_BRIGHT_BLACK = "100"
    BG_BRIGHT_RED = "101"
    BG_BRIGHT_GREEN = "102"
    BG_BRIGHT_YELLOW = "103"
    BG_BRIGHT_BLUE = "104"
    BG_BRIGHT_MAGENTA = "105"
    BG_BRIGHT_CYAN = "106"
    BG_BRIGHT_WHITE = "107"
```

## Align Enum

The `Align` enum defines text alignment options for the `styled` function.

```python
class Align(Enum):
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
```

| Value | Description |
|-------|-------------|
| `Align.LEFT` | Aligns text to the left (default) |
| `Align.RIGHT` | Aligns text to the right |
| `Align.CENTER` | Centers text |

## tabled Function

```python
def tabled(
    headers: List[str],
    rows: List[List[Any]],
    column_styles: Optional[List[StyleType]] = None,
    header_style: StyleType = Style.BOLD,
    widths: Optional[List[int]] = None,
    alignments: Optional[List[Align]] = None,
    borders: bool = True,
    highlight_rows: Optional[List[int]] = None,
    highlight_style: StyleType = Style.REVERSE,
    cell_formatter: Optional[Callable] = None,
    style: str = "default",
) -> str:
    """
    Create a formatted table with headers and rows.
    """
```

Creates a formatted table with headers and rows.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `headers` | `List[str]` | List of header strings |
| `rows` | `List[List[Any]]` | List of rows, where each row is a list of values |
| `column_styles` | `Optional[List[StyleType]]` | Optional list of styles to apply to each column |
| `header_style` | `StyleType` | Style to apply to the header row (default: `Style.BOLD`) |
| `widths` | `Optional[List[int]]` | Optional list of column widths |
| `alignments` | `Optional[List[Align]]` | Optional list of column alignments |
| `borders` | `bool` | Whether to display borders with Unicode box-drawing characters (default: `True`) |
| `highlight_rows` | `Optional[List[int]]` | Optional list of row indices to highlight |
| `highlight_style` | `StyleType` | Style to apply to highlighted rows (default: `Style.REVERSE`) |
| `cell_formatter` | `Optional[Callable]` | Optional function to format cell values |
| `style` | `str` | Table style ("default", "compact", or "thin") |

### Table Styles

| Style | Description |
|-------|-------------|
| `"default"` | Standard table with Unicode borders and a separator line between headers and data |
| `"compact"` | No borders, with bold and underlined headers |
| `"thin"` | Unicode borders but no separator line between headers and data, with bold and underlined headers |

### Returns

A formatted table as a string.

### Example

```python
from charstyle import tabled, Style, Align

headers = ["ID", "Name", "Status"]
rows = [
    ["1", "Alice Smith", "Active"],
    ["2", "Bob Johnson", "Inactive"],
]

# Default style (Unicode borders)
print(tabled(
    headers,
    rows,
    widths=[5, 20, 10],
    alignments=[Align.CENTER, Align.LEFT, Align.CENTER]
))

# Compact style (no borders)
print(tabled(
    headers,
    rows,
    style="compact",
    borders=False
))

# Thin style (no header separator)
print(tabled(
    headers,
    rows,
    style="thin"
))
```

Output (Default style):
```
┌───────┬──────────────────────┬────────────┐
│  ID   │ Name                 │   Status   │
├───────┼──────────────────────┼────────────┤
│  1    │ Alice Smith          │   Active   │
│  2    │ Bob Johnson          │  Inactive  │
└───────┴──────────────────────┴────────────┘
```

Output (Compact style):
```
ID Name                 Status
1  Alice Smith          Active
2  Bob Johnson          Inactive
```

Output (Thin style):
```
┌───────┬──────────────────────┬────────────┐
│  ID   │ Name                 │   Status   │
│  1    │ Alice Smith          │   Active   │
│  2    │ Bob Johnson          │  Inactive  │
└───────┴──────────────────────┴────────────┘
```

## supports_color

Check if the terminal supports color.

```python
supports_color() -> bool
```

**Returns:**
- `bool`: True if the terminal supports color, False otherwise

**Example:**
```python
from charstyle import supports_color

if supports_color():
    print("Terminal supports color")
else:
    print("Terminal does not support color")
