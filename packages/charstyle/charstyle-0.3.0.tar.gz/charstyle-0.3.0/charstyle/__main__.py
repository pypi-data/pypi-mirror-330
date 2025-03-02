#!/usr/bin/env python3
"""
Main module for charstyle package.
When run as `python -m charstyle`, this will display a summary of available commands.
When run as `python -m charstyle styles`, this will display a sample of all available styles.
When run as `python -m charstyle icons`, this will display available terminal icons.
When run as `python -m charstyle tables`, this will display table formatting examples.
When run as `python -m charstyle tables [style]`, this will display a specific table style.
"""

import argparse

from charstyle import Style, styled


def show_summary() -> None:
    """Display a summary of available charstyle commands."""
    print(styled("\n=== charstyle CLI ===", Style.BOLD))
    print("A library for styling terminal text using ANSI escape sequences\n")

    print(styled("Available Commands:", Style.BOLD))
    print(f"  {styled('styles', Style.CYAN)} - Display all available text styles")
    print(f"  {styled('icons', Style.CYAN)} - Display all available terminal icons")
    print(f"  {styled('icons [category]', Style.CYAN)} - Display icons from a specific category")
    print(f"  {styled('tables', Style.CYAN)} - Display all table formatting examples")
    print(
        f"  {styled('tables [style]', Style.CYAN)} - Display a specific table style (default, compact, thin)\n"
    )

    print(styled("Examples:", Style.BOLD))
    print(f"  python -m charstyle {styled('styles', Style.CYAN)}")
    print(f"  python -m charstyle {styled('icons Hearts', Style.CYAN)}")
    print(f"  python -m charstyle {styled('tables thin', Style.CYAN)}\n")

    print(
        f"For more information, visit: {styled('https://github.com/joaompinto/charstyle', (Style.BLUE, Style.UNDERLINE))}"
    )


def main() -> None:
    """Main function for the charstyle CLI."""
    parser = argparse.ArgumentParser(description="Terminal styling utilities")

    # Create subparsers for the different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Styles command
    _ = subparsers.add_parser("styles", help="Display available text styles")

    # Icons command
    icons_parser = subparsers.add_parser("icons", help="Display available terminal icons")
    icons_parser.add_argument("category", nargs="?", help="Show icons from a specific category")

    # Tables command
    tables_parser = subparsers.add_parser("tables", help="Display table formatting examples")
    tables_parser.add_argument(
        "style",
        nargs="?",
        choices=["default", "compact", "thin"],
        help="Show a specific table style",
    )

    args = parser.parse_args()

    if args.command == "styles":
        from charstyle.cli.styles_display import show_styles

        show_styles()
    elif args.command == "icons":
        from charstyle.cli.icons_display import show_category, show_icons

        if hasattr(args, "category") and args.category:
            show_category(args.category)
        else:
            show_icons()
    elif args.command == "tables":
        from charstyle.cli.tables_display import show_specific_style, show_tables

        if hasattr(args, "style") and args.style:
            show_specific_style(args.style)
        else:
            show_tables()
    else:
        show_summary()


if __name__ == "__main__":
    main()
