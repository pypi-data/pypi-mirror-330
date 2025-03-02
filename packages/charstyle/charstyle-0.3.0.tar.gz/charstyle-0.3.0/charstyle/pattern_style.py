"""
Pattern-based styling functions for the charstyle library.

This module provides functions for styling text based on patterns and delimiters.
"""

import re
from re import Pattern
from typing import Any

from charstyle.charstyle import styled
from charstyle.styles import Style

# Type alias for style parameters
StyleType = Style | tuple[Style, ...]


def styled_split(text: str, delimiter: str, *styles: StyleType) -> str:
    """
    Split text by a delimiter and apply different styles to each part.

    Args:
        text (str): The text to style
        delimiter (str): The delimiter to split on
        *styles: Variable number of style constants to apply to each part

    Returns:
        str: The styled text

    Raises:
        ValueError: If the number of styles doesn't match the number of parts after splitting

    Example:
        >>> from charstyle import Style
        >>> styled_split("Status: OK", ":", Style.RED, Style.GREEN)
        # This returns "Status" in red and " OK" in green
    """
    # Return empty string for empty input
    if not text:
        return ""

    parts = text.split(delimiter)

    # Check if the number of parts matches the number of styles
    if len(parts) != len(styles):
        raise ValueError(
            f"Number of parts ({len(parts)}) doesn't match number of styles ({len(styles)})"
        )

    styled_parts = []

    for i, part in enumerate(parts):
        style = styles[i]
        styled_parts.append(styled(part, style))

    return delimiter.join(styled_parts)


def styled_pattern(text: str, pattern: str | Pattern, *styles: StyleType) -> str:
    """
    Style text by splitting it with a regex pattern and applying different styles to each captured group.

    Args:
        text (str): The text to style
        pattern (str | Pattern): The regex pattern to match
        *styles: Variable number of style constants to apply to each captured group

    Returns:
        str: The styled text

    Example:
        >>> from charstyle import Style
        >>> styled_pattern("Hello World", r"(World)", Style.RED)
        # This returns "Hello " and "World" in red
    """
    # Compile the pattern if it's a string
    if isinstance(pattern, str):
        pattern = re.compile(pattern)

    matches = list(pattern.finditer(text))
    if not matches:
        return text

    # Create a list to hold the result
    result_list = []
    last_end = 0

    for match in matches:
        # Add the text before the match
        if match.start() > last_end:
            result_list.append(text[last_end : match.start()])

        # Add the styled captured groups
        for i, group in enumerate(match.groups(), start=1):
            if group is not None:
                if i - 1 < len(styles):
                    result_list.append(styled(group, styles[i - 1]))
                else:
                    result_list.append(group)

        last_end = match.end()

    # Add any remaining text
    if last_end < len(text):
        result_list.append(text[last_end:])

    return "".join(result_list)


def styled_pattern_match(text: str, pattern: str | Pattern, style_map: dict[str, StyleType]) -> str:
    """
    Style text by matching a regex pattern with named groups and applying styles from a style map.

    Args:
        text (str): The text to style
        pattern (str | Pattern): The regex pattern with named groups to match
        style_map (Dict[str, StyleType]): A mapping of group names to styles

    Returns:
        str: The styled text

    Example:
        >>> from charstyle import Style
        >>> pattern = r"(?P<n>[a-z]+): (?P<value>\d+)"
        >>> style_map = {"n": Style.RED, "value": Style.GREEN}
        >>> styled_pattern_match("Count: 42", pattern, style_map)
        # This returns "Count" in red and "42" in green
    """
    # Compile the pattern if it's a string
    if isinstance(pattern, str):
        pattern = re.compile(pattern)

    match = pattern.search(text)
    if not match:
        return text

    # Create a list to hold the result
    result_list = []
    last_end = 0

    # Process all named groups
    for group_name, style in style_map.items():
        try:
            group_start = match.start(group_name)
            group_end = match.end(group_name)
            group_text = match.group(group_name)

            # Add any text before this group
            if group_start > last_end:
                result_list.append(text[last_end:group_start])

            # Add the styled group
            result_list.append(styled(group_text, style))

            # Update last_end if this group ends later
            last_end = max(last_end, group_end)
        except IndexError:
            # Group not found, skip it
            continue

    # Add any remaining text
    if last_end < len(text):
        result_list.append(text[last_end:])

    return "".join(result_list)


def styled_format(
    format_str: str, *args: tuple[Any, StyleType], **kwargs: tuple[Any, StyleType]
) -> str:
    """
    Format a string with styled values, similar to str.format().

    Args:
        format_str (str): The format string with placeholders
        *args: Positional arguments as tuples of (value, style)
        **kwargs: Keyword arguments as tuples of (value, style)

    Returns:
        str: The formatted string with styled values

    Example:
        >>> from charstyle import Style
        >>> styled_format("{} {}", ("Hello", Style.RED), ("World", Style.GREEN))
        # This returns "Hello" in red and "World" in green
    """
    # Process positional arguments
    styled_args = []
    for arg in args:
        value, style = arg
        styled_args.append(styled(str(value), style))

    # Process keyword arguments
    styled_kwargs = {}
    for key, arg in kwargs.items():
        value, style = arg
        styled_kwargs[key] = styled(str(value), style)

    # Format the string
    return format_str.format(*styled_args, **styled_kwargs)
