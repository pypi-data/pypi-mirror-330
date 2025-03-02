"""
Tests for the color support caching mechanism.
"""

import os
import unittest
from unittest.mock import patch

import charstyle.charstyle
from charstyle.charstyle import styled, supports_color
from charstyle.styles import Style


class TestColorCaching(unittest.TestCase):
    """Test the color support caching mechanism."""

    def setUp(self):
        """Reset the global color support cache before each test."""
        # Reset the global cache
        charstyle.charstyle._SUPPORTS_COLOR = None

        # Clear the lru_cache
        supports_color.cache_clear()

    def test_supports_color_caching(self):
        """Test that the color support check is cached."""
        # First call should determine the value
        initial_value = supports_color()

        # Modify the environment to force a different result
        # but the cached value should be used
        with patch.dict(os.environ, {"NO_COLOR": "1"}):
            # Second call should use the cached value
            self.assertEqual(supports_color(), initial_value)

        # After clearing the cache, the new environment should be used
        supports_color.cache_clear()
        charstyle.charstyle._SUPPORTS_COLOR = None

        with patch.dict(os.environ, {"NO_COLOR": "1"}):
            self.assertFalse(supports_color())

    def test_styled_uses_cached_color_support(self):
        """Test that the styled function uses the cached color support value."""
        # Force color support to be True
        with patch("charstyle.charstyle.supports_color", return_value=True):
            # Style should be applied
            result = styled("test", Style.RED)
            self.assertNotEqual(result, "test")
            self.assertIn("\033[", result)

        # Force color support to be False
        with patch("charstyle.charstyle.supports_color", return_value=False):
            # Style should not be applied
            result = styled("test", Style.RED)
            self.assertEqual(result, "test")
            self.assertNotIn("\033[", result)


if __name__ == "__main__":
    unittest.main()
