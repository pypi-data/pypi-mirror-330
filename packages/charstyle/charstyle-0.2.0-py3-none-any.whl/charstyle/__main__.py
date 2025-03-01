#!/usr/bin/env python3
"""
Main module for charstyle package.
When run as `python -m charstyle`, this will display a sample of all available styles.
When run as `python -m charstyle --icons`, this will display available terminal icons.
"""
import argparse


def main() -> None:
    """Main function for the charstyle CLI."""
    parser = argparse.ArgumentParser(description="Terminal styling utilities")
    parser.add_argument("--icons", action="store_true", help="Display available terminal icons")

    args = parser.parse_args()

    if args.icons:
        from charstyle.cli.icons_display import show_icons

        show_icons()
    else:
        from charstyle.cli.styles_display import show_styles

        show_styles()


if __name__ == "__main__":
    main()
