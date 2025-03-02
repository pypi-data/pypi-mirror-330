#!/usr/bin/env python3
"""
Example script demonstrating a dashboard-like application using the charstyle library.
"""

import time
from datetime import datetime
from random import randint

from charstyle import Align, Style, styled, tabled


def generate_system_stats():
    """Generate random system statistics for the example."""
    return {
        "cpu": randint(5, 95),
        "memory": randint(20, 85),
        "disk": randint(30, 90),
        "network": randint(1, 100),
        "temperature": randint(35, 75),
    }


def generate_service_status():
    """Generate random service statuses for the example."""
    services = ["Web Server", "Database", "Cache", "API Gateway", "Auth Service"]
    statuses = ["Running", "Running", "Running", "Running", "Running"]

    # Randomly set some services to different states
    for i in range(len(services)):
        if randint(1, 10) == 1:
            statuses[i] = "Warning"
        elif randint(1, 20) == 1:
            statuses[i] = "Error"

    return list(zip(services, statuses, strict=False))


def format_status(status):
    """Format a status string with appropriate styling."""
    if status == "Running":
        return styled(status, Style.GREEN)
    elif status == "Warning":
        return styled(status, Style.YELLOW)
    else:
        return styled(status, Style.RED)


def format_usage(value):
    """Format a usage value with appropriate styling based on thresholds."""
    if value < 50:
        return styled(f"{value}%", Style.GREEN)
    elif value < 80:
        return styled(f"{value}%", Style.YELLOW)
    else:
        return styled(f"{value}%", Style.RED)


def display_header():
    """Display a styled header for the dashboard."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(
        "\n" + styled(" System Dashboard ", Style.BOLD, width=80, align=Align.CENTER, fill_char="=")
    )
    print(styled(f" Last Updated: {current_time} ", Style.ITALIC, width=80, align=Align.RIGHT))
    print()


def display_system_stats(stats):
    """Display system statistics in a styled table."""
    headers = ["Metric", "Usage", "Status"]
    rows = [
        ["CPU", format_usage(stats["cpu"]), get_status_bar(stats["cpu"])],
        ["Memory", format_usage(stats["memory"]), get_status_bar(stats["memory"])],
        ["Disk", format_usage(stats["disk"]), get_status_bar(stats["disk"])],
        ["Network", format_usage(stats["network"]), get_status_bar(stats["network"])],
        ["Temperature", format_usage(stats["temperature"]), get_status_bar(stats["temperature"])],
    ]

    print(styled(" System Statistics ", Style.BOLD, width=80, align=Align.LEFT, fill_char="-"))
    print(
        tabled(
            headers,
            rows,
            header_style=Style.BOLD,
            widths=[15, 10, 50],
            alignments=[Align.LEFT, Align.CENTER, Align.LEFT],
            borders=True,
            style="ascii",
        )
    )
    print()


def display_service_status(services):
    """Display service statuses in a styled table."""
    headers = ["Service", "Status", "Last Check"]
    rows = []

    for service, status in services:
        rows.append([service, format_status(status), datetime.now().strftime("%H:%M:%S")])

    print(styled(" Service Status ", Style.BOLD, width=80, align=Align.LEFT, fill_char="-"))
    print(
        tabled(
            headers,
            rows,
            header_style=Style.BOLD,
            widths=[20, 15, 15],
            alignments=[Align.LEFT, Align.CENTER, Align.CENTER],
            borders=True,
            style="ascii",
        )
    )
    print()


def get_status_bar(value, width=40):
    """Create a visual status bar with color coding."""
    filled_width = int(width * value / 100)
    empty_width = width - filled_width

    if value < 50:
        bar = styled("█" * filled_width, Style.GREEN)
    elif value < 80:
        bar = styled("█" * filled_width, Style.YELLOW)
    else:
        bar = styled("█" * filled_width, Style.RED)

    return bar + styled("░" * empty_width, Style.DIM)


def display_footer():
    """Display a styled footer for the dashboard."""
    print(
        styled(" Press Ctrl+C to exit ", Style.ITALIC, width=80, align=Align.CENTER, fill_char="-")
    )
    print()


def main():
    """Run the dashboard example."""
    try:
        while True:
            # Clear screen (works on most terminals)
            print("\033c", end="")

            # Generate random data
            stats = generate_system_stats()
            services = generate_service_status()

            # Display dashboard
            display_header()
            display_system_stats(stats)
            display_service_status(services)
            display_footer()

            # Update every 2 seconds
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nExiting dashboard example.")


if __name__ == "__main__":
    main()
