"""
Tests for the core charstyle functionality.
"""

import os
import unittest
from unittest.mock import patch

import charstyle.charstyle
from charstyle import Style, styled
from charstyle.charstyle import supports_color


class TestCharstyle(unittest.TestCase):
    """Test cases for the charstyle module."""

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

    def test_styled_basic(self):
        """Test the basic functionality of the styled function."""
        # Test with a single style
        result = styled("Hello", Style.RED)
        expected = "\033[31mHello\033[0m"
        self.assertEqual(result, expected)

    def test_styled_multiple_styles(self):
        """Test styled with multiple styles."""
        # Test with multiple styles
        result = styled("Hello", (Style.BOLD, Style.RED))
        expected = "\033[1;31mHello\033[0m"
        self.assertEqual(result, expected)

        # Test with three styles
        result = styled("Hello", (Style.BOLD, Style.UNDERLINE, Style.RED))
        expected = "\033[1;4;31mHello\033[0m"
        self.assertEqual(result, expected)

    def test_styled_with_background(self):
        """Test styled with background colors."""
        # Test with foreground and background
        result = styled("Hello", (Style.RED, Style.BG_BLUE))
        expected = "\033[31;44mHello\033[0m"
        self.assertEqual(result, expected)

    def test_styled_with_bright_colors(self):
        """Test styled with bright colors."""
        # Test with bright foreground
        result = styled("Hello", Style.BRIGHT_RED)
        expected = "\033[91mHello\033[0m"
        self.assertEqual(result, expected)

        # Test with bright background
        result = styled("Hello", Style.BG_BRIGHT_GREEN)
        expected = "\033[102mHello\033[0m"
        self.assertEqual(result, expected)

    def test_styled_no_color_support(self):
        """Test styled when color is not supported."""
        # Mock supports_color to return False
        with patch("charstyle.charstyle.supports_color", return_value=False):
            result = styled("Hello", Style.RED)
            expected = "Hello"
            self.assertEqual(result, expected)

    def test_supports_color(self):
        """Test the supports_color function."""
        # Reset the global cache and clear the lru_cache
        charstyle.charstyle._SUPPORTS_COLOR = None
        supports_color.cache_clear()

        # With FORCE_COLOR set, should return True
        self.assertTrue(supports_color())

        # Reset the global cache and clear the lru_cache
        charstyle.charstyle._SUPPORTS_COLOR = None
        supports_color.cache_clear()

        # With NO_COLOR set, should return False
        os.environ["NO_COLOR"] = "1"
        self.assertFalse(supports_color())
        del os.environ["NO_COLOR"]


if __name__ == "__main__":
    unittest.main()
