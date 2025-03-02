"""
Tests for the complex styling functionality in charstyle.
"""

import os
import unittest
from unittest.mock import patch

import charstyle.charstyle
from charstyle import Style
from charstyle.charstyle import supports_color
from charstyle.pattern_style import (
    styled_format,
    styled_pattern,
    styled_pattern_match,
    styled_split,
)


class TestComplexStyle(unittest.TestCase):
    """Test cases for the complex styling functionality."""

    def setUp(self):
        """Set up the test environment."""
        # Reset the global cache
        charstyle.charstyle._SUPPORTS_COLOR = None

        # Clear the lru_cache
        supports_color.cache_clear()

        # Force color support for testing
        os.environ["FORCE_COLOR"] = "1"
        # Ensure sys.stdout.isatty() returns True
        self.isatty_patcher = patch("sys.stdout.isatty", return_value=True)
        self.isatty_mock = self.isatty_patcher.start()

    def tearDown(self):
        """Clean up the test environment."""
        # Remove the environment variable
        if "FORCE_COLOR" in os.environ:
            del os.environ["FORCE_COLOR"]
        # Stop the patch
        self.isatty_patcher.stop()

    def test_styled_split(self):
        """Test the styled_split function."""
        # Test with a simple delimiter
        result = styled_split("Hello World", " ", Style.RED, Style.GREEN)
        expected = "\033[31mHello\033[0m \033[32mWorld\033[0m"
        self.assertEqual(result, expected)

        # Test with a delimiter that appears multiple times
        result = styled_split("a,b,c", ",", Style.RED, Style.GREEN, Style.BLUE)
        expected = "\033[31ma\033[0m,\033[32mb\033[0m,\033[34mc\033[0m"
        self.assertEqual(result, expected)

        # Test with a delimiter that doesn't appear
        result = styled_split("Hello", ",", Style.RED)
        expected = "\033[31mHello\033[0m"
        self.assertEqual(result, expected)

        # Test with an empty string
        result = styled_split("", ",", Style.RED)
        expected = ""
        self.assertEqual(result, expected)

        # Test with multiple styles
        result = styled_split(
            "Hello World", " ", (Style.BOLD, Style.RED), (Style.ITALIC, Style.GREEN)
        )
        expected = "\033[1;31mHello\033[0m \033[3;32mWorld\033[0m"
        self.assertEqual(result, expected)

        # Test with mismatched styles and parts
        with self.assertRaises(ValueError):
            styled_split("a,b,c", ",", Style.RED, Style.GREEN)

    def test_styled_pattern(self):
        """Test the styled_pattern function."""
        # Test with a simple pattern
        result = styled_pattern("Hello World", r"(World)", Style.RED)
        expected = "Hello \033[31mWorld\033[0m"
        self.assertEqual(result, expected)

        # Test with a pattern that doesn't match
        result = styled_pattern("Hello World", r"(Universe)", Style.RED)
        expected = "Hello World"
        self.assertEqual(result, expected)

        # Test with a pattern that matches multiple times
        result = styled_pattern("Hello Hello World", r"(Hello)", Style.RED)
        expected = "\033[31mHello\033[0m \033[31mHello\033[0m World"
        self.assertEqual(result, expected)

        # Test with multiple styles
        result = styled_pattern("Hello World", r"(World)", (Style.BOLD, Style.RED))
        expected = "Hello \033[1;31mWorld\033[0m"
        self.assertEqual(result, expected)

    def test_styled_pattern_match(self):
        """Test the styled_pattern_match function."""
        # Test with named groups
        pattern = r"(?P<salutation>Hello) (?P<n>World)"
        style_map = {"salutation": Style.RED, "n": Style.GREEN}
        result = styled_pattern_match("Hello World", pattern, style_map)
        expected = "\033[31mHello\033[0m \033[32mWorld\033[0m"
        self.assertEqual(result, expected)

        # Test with pattern that doesn't match
        pattern = r"(?P<salutation>Goodbye) (?P<n>World)"
        style_map = {"salutation": Style.RED, "n": Style.GREEN}
        result = styled_pattern_match("Hello World", pattern, style_map)
        expected = "Hello World"
        self.assertEqual(result, expected)

        # Test with pattern that has more groups than styles
        pattern = r"(?P<salutation>Hello) (?P<n>World)"
        style_map = {"salutation": Style.RED}
        result = styled_pattern_match("Hello World", pattern, style_map)
        expected = "\033[31mHello\033[0m World"
        self.assertEqual(result, expected)

        # Test with multiple styles per group
        pattern = r"(?P<salutation>Hello) (?P<n>World)"
        style_map = {"salutation": (Style.BOLD, Style.RED), "n": (Style.ITALIC, Style.GREEN)}
        result = styled_pattern_match("Hello World", pattern, style_map)
        expected = "\033[1;31mHello\033[0m \033[3;32mWorld\033[0m"
        self.assertEqual(result, expected)

    def test_styled_format(self):
        """Test the styled_format function."""
        # Test with positional arguments
        result = styled_format("{} {}", ("Hello", Style.RED), ("World", Style.GREEN))
        expected = "\033[31mHello\033[0m \033[32mWorld\033[0m"
        self.assertEqual(result, expected)

        # Test with keyword arguments
        result = styled_format(
            "{greeting} {name}", greeting=("Hello", Style.RED), name=("World", Style.GREEN)
        )
        expected = "\033[31mHello\033[0m \033[32mWorld\033[0m"
        self.assertEqual(result, expected)

        # Test with mixed arguments
        result = styled_format("{0} {name}", ("Hello", Style.RED), name=("World", Style.GREEN))
        expected = "\033[31mHello\033[0m \033[32mWorld\033[0m"
        self.assertEqual(result, expected)

        # Test with multiple styles per argument
        result = styled_format(
            "{} {}", ("Hello", (Style.BOLD, Style.RED)), ("World", (Style.ITALIC, Style.GREEN))
        )
        expected = "\033[1;31mHello\033[0m \033[3;32mWorld\033[0m"
        self.assertEqual(result, expected)

        # Test with a colon in the format string
        result = styled_format("{}:{}", ("Hello", Style.RED), ("World", Style.GREEN))
        expected = "\033[31mHello\033[0m:\033[32mWorld\033[0m"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
