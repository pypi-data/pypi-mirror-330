#!/usr/bin/env python3
"""
Practical examples demonstrating real-world applications of charstyle's styling capabilities.
"""

import time
from datetime import datetime

from charstyle import (
    Style,
    styled,
    supports_color,
)


def simulated_log_output() -> None:
    """Simulates a log output with different log levels styled appropriately."""
    print("\n=== Log Output Example ===")

    # Define log level styles as tuples
    debug_style = (Style.BRIGHT_BLACK,)
    info_style = (Style.BRIGHT_BLUE,)
    warning_style = (Style.YELLOW,)
    error_style = (Style.BRIGHT_RED,)
    critical_style = (Style.BRIGHT_WHITE, Style.BG_RED, Style.BOLD)
    timestamp_style = (Style.BRIGHT_BLACK,)

    # Simulate log entries
    log_entries = [
        ("DEBUG", debug_style, "Connection pool initialized with 5 connections"),
        ("INFO", info_style, "Server started on port 8080"),
        ("WARNING", warning_style, "High memory usage detected: 85%"),
        ("ERROR", error_style, "Failed to connect to database: Connection refused"),
        ("CRITICAL", critical_style, "System shutdown initiated due to disk failure"),
    ]

    # Display log entries
    for level, style, message in log_entries:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        formatted_timestamp = styled(timestamp, timestamp_style)
        formatted_level = styled(f"[{level}]".ljust(10), style)
        print(f"{formatted_timestamp} {formatted_level} {message}")


def system_status_dashboard() -> None:
    """Displays a system status dashboard with styled components."""
    print("\n=== System Status Dashboard Example ===")

    # Define status styles
    ok_style = (Style.GREEN, Style.BOLD)
    warning_style = (Style.YELLOW, Style.BOLD)
    critical_style = (Style.RED, Style.BOLD)
    header_style = (Style.BRIGHT_WHITE, Style.BG_BLUE, Style.BOLD)
    label_style = (Style.BRIGHT_BLACK,)

    # Display dashboard header
    print(styled(" SYSTEM STATUS DASHBOARD ".center(60), header_style))
    print()

    # System components and their statuses
    components = [
        ("CPU Usage", "32%", ok_style),
        ("Memory", "4.2GB/8GB (52%)", ok_style),
        ("Disk Space", "120GB/500GB (24%)", ok_style),
        ("Network", "84Mbps Down / 12Mbps Up", ok_style),
        ("Database", "WARN: High query time", warning_style),
        ("Web Server", "ERROR: 3 failed requests", critical_style),
    ]

    # Display component statuses
    for component, status, style in components:
        label = styled(f"{component}:".ljust(20), label_style)
        status_text = styled(status, style)
        print(f"{label} {status_text}")


def interactive_cli_menu() -> None:
    """Simulates an interactive CLI menu with styled options."""
    print("\n=== Interactive CLI Menu Example ===")

    # Define menu styles
    title_style = (Style.BRIGHT_WHITE, Style.BG_BLUE, Style.BOLD)
    option_style = (Style.BRIGHT_CYAN,)
    key_style = (Style.YELLOW, Style.BOLD)
    description_style = (Style.WHITE,)
    selected_style = (Style.BLACK, Style.BG_GREEN)
    footer_style = (Style.BRIGHT_BLACK, Style.ITALIC)

    # Display menu title
    print(styled(" FILE OPERATIONS ".center(50), title_style))
    print()

    # Menu options
    options = [
        ("1", "Open File", "Open an existing file for editing"),
        ("2", "Save", "Save current file"),
        ("3", "Save As", "Save current file with a new name"),
        ("4", "Export", "Export file to different format"),
        ("5", "Print", "Send file to printer"),
        ("q", "Quit", "Exit the application"),
    ]

    # Display menu options
    for key, option, description in options:
        formatted_key = styled(f"[{key}]", key_style)
        formatted_option = styled(option.ljust(10), option_style)
        formatted_description = styled(description, description_style)
        print(f"  {formatted_key} {formatted_option} {formatted_description}")

    print()
    print(styled("Enter your choice: ", option_style), end="")

    # Simulate user selection (for demo purposes)
    selected = "2"
    print(styled(selected, selected_style))
    print()
    print(styled("Saving file...", (Style.GREEN,)))
    print(styled("File saved successfully!", (Style.GREEN, Style.BOLD)))
    print()
    print(styled("Press any key to continue...", footer_style))


def main() -> None:
    """Run all practical examples."""
    if not supports_color():
        print("Your terminal does not support colors.")
        return

    simulated_log_output()
    time.sleep(1)  # Pause for readability

    system_status_dashboard()
    time.sleep(1)  # Pause for readability

    interactive_cli_menu()


if __name__ == "__main__":
    main()
