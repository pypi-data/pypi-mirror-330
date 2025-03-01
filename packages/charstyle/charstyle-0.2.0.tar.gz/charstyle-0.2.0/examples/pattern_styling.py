#!/usr/bin/env python3
"""
Example script demonstrating complex string styling in charstyle.
"""

from charstyle import (
    Style,
    styled_format,
    styled_pattern,
    styled_split,
    supports_color,
)


def main() -> None:
    """
    Demonstrate the complex styling features.
    """
    # Check if terminal supports colors
    if not supports_color():
        print("Your terminal does not support colors.")
        return

    print("\n=== Styled Split Examples ===")

    # Split by delimiter and style each part differently
    print(styled_split("Status: OK", ":", Style.BLUE, Style.GREEN))

    # Another example with error message
    print(styled_split("Error: File not found", ":", Style.RED, (Style.ITALIC,)))

    # Using predefined styles
    key_style = (Style.CYAN, Style.BOLD)
    value_style = (Style.BRIGHT_GREEN,)
    print(styled_split("debug_mode = True", " = ", key_style, value_style))

    print("\n=== Styled Pattern Examples ===")

    # The styled_pattern function splits the text based on the regex pattern
    # and applies different styles to each part

    # Example 1: Style different parts of a log message
    log_message = "2023-04-15 14:30:45 [INFO] User logged in successfully"

    # Style the timestamp, log level, and message differently
    print(
        styled_pattern(
            log_message,
            r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})|(\[\w+\])|(.+)",
            Style.BLUE,  # timestamp
            (Style.YELLOW, Style.BOLD),  # log level
            Style.WHITE,  # message
        )
    )

    # Example 2: Style a configuration file line
    config_line = "server_port=8080 # Default HTTP port"

    # Style the key, value, and comment differently
    print(
        styled_pattern(
            config_line,
            r"([a-z_]+)|(=)|(\d+)|( # )|(.+)",
            (Style.YELLOW, Style.BOLD),  # key
            Style.WHITE,  # equals sign
            (Style.BRIGHT_GREEN,),  # value
            Style.WHITE,  # comment marker
            (Style.BRIGHT_BLUE, Style.ITALIC),  # comment text
        )
    )

    print("\n=== Styled Format Examples ===")

    # Example 1: Format a user info string
    username = "admin"
    ip_address = "192.168.1.100"
    login_time = "2023-04-15 15:45:22"

    # Format with styled components
    user_info = styled_format(
        "User {username} logged in from {ip} at {time}",
        username=(username, (Style.BRIGHT_GREEN, Style.BOLD)),
        ip=(ip_address, Style.RED),
        time=(login_time, Style.BLUE),
    )
    print(user_info)

    # Example 2: Format a command example
    command = styled_format(
        "{cmd} {arg1} {arg2}",
        cmd=("git", (Style.YELLOW, Style.BOLD)),
        arg1=("commit", Style.CYAN),
        arg2=("-m 'Update README'", Style.GREEN),
    )
    print(f"Run this command: {command}")


if __name__ == "__main__":
    main()
