#!/usr/bin/env python3
"""
Example of using the charstyle Icon enum.
This demonstrates how to use terminal icons for status indicators, progress bars,
and simple UI elements.
"""

from charstyle import (
    Icon,
    Style,
    styled,
    supports_color,
)


def main() -> None:
    """Main demo function for charstyle icons."""
    # Check if terminal supports colors
    if not supports_color():
        print("Your terminal doesn't support colors. Examples may not display correctly.")
        return

    print("\n=== charstyle Icons Demo ===\n")

    # Status indicators
    print(styled("Status Indicators:", Style.BOLD))
    print(f"{styled(Icon.CHECK, Style.GREEN)} {styled('Success:', Style.BOLD)} Operation completed")
    print(f"{styled(Icon.CROSS, Style.RED)} {styled('Error:', Style.BOLD)} File not found")
    print(
        f"{styled(Icon.WARNING, Style.YELLOW)} {styled('Warning:', Style.BOLD)} Disk space is low"
    )
    print(
        f"{styled(Icon.INFO, Style.BLUE)} {styled('Info:', Style.BOLD)} System is running normally"
    )
    print()

    # Progress bar with icons
    progress = 7
    bar = Icon.BLOCK * progress + Icon.LIGHT_SHADE * (10 - progress)
    print(styled("Progress Bar:", Style.BOLD))
    print(f"Loading: [{styled(bar, Style.GREEN)}] {progress * 10}%")
    print()

    # Box drawing with icons
    print(styled("Box Drawing:", Style.BOLD))
    print(f"{Icon.TOP_LEFT}{Icon.H_LINE * 20}{Icon.TOP_RIGHT}")
    print(f"{Icon.V_LINE} {styled('Menu', Style.BOLD)}               {Icon.V_LINE}")
    print(f"{Icon.T_RIGHT}{Icon.H_LINE * 20}{Icon.T_LEFT}")
    print(f"{Icon.V_LINE} {styled('1.', Style.GREEN)} New File        {Icon.V_LINE}")
    print(f"{Icon.V_LINE} {styled('2.', Style.GREEN)} Open File       {Icon.V_LINE}")
    print(f"{Icon.V_LINE} {styled('3.', Style.GREEN)} Save            {Icon.V_LINE}")
    print(f"{Icon.V_LINE} {styled('4.', Style.GREEN)} Exit            {Icon.V_LINE}")
    print(f"{Icon.BOTTOM_LEFT}{Icon.H_LINE * 20}{Icon.BOTTOM_RIGHT}")
    print()

    # Bullet points with icons
    print(styled("Bullet Points:", Style.BOLD))
    print(f"{Icon.CIRCLE} First item")
    print(f"{Icon.CIRCLE} Second item")
    print(f"{Icon.CIRCLE} Third item")
    print()

    # Arrows and directional indicators
    print(styled("Arrows:", Style.BOLD))
    print(f"{Icon.ARROW_RIGHT} Next")
    print(f"{Icon.ARROW_LEFT} Previous")
    print(f"{Icon.ARROW_UP} Up")
    print(f"{Icon.ARROW_DOWN} Down")
    print()


if __name__ == "__main__":
    main()
