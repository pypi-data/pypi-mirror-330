"""
Icon display functionality for charstyle CLI.
This module provides functions to display terminal icons.
"""

from collections.abc import Callable

from charstyle import Style, styled
from charstyle.icons import Icon


def show_icons() -> None:
    """
    Display all available terminal icons.

    This function prints all available terminal icons, organized by category.
    Each category is displayed with a different color scheme.
    """

    # Create style functions
    def bold(text: str) -> str:
        return styled(text, Style.BOLD)

    def blue(text: str) -> str:
        return styled(text, Style.BLUE)

    def green(text: str) -> str:
        return styled(text, Style.GREEN)

    def red(text: str) -> str:
        return styled(text, Style.RED)

    def yellow(text: str) -> str:
        return styled(text, Style.YELLOW)

    def cyan(text: str) -> str:
        return styled(text, Style.CYAN)

    def magenta(text: str) -> str:
        return styled(text, Style.MAGENTA)

    # Define category colors
    category_styles = get_category_styles(green, red, yellow, cyan, blue, magenta)
    categories = get_icon_categories()

    # Display icons by category
    for category, icon_names in categories.items():
        icons_sequence = ""
        for i, name in enumerate(icon_names):
            icon = getattr(Icon, name)
            style_fn = category_styles[category][i % len(category_styles[category])]
            icons_sequence += f"{style_fn(icon)} "
        print(f"{bold(category)}: {icons_sequence.strip()}")


def show_category(category: str) -> None:
    """
    Display terminal icons from a specific category.

    Args:
        category: The category name to display icons from
    """

    # Create style functions
    def bold(text: str) -> str:
        return styled(text, Style.BOLD)

    def blue(text: str) -> str:
        return styled(text, Style.BLUE)

    def green(text: str) -> str:
        return styled(text, Style.GREEN)

    def red(text: str) -> str:
        return styled(text, Style.RED)

    def yellow(text: str) -> str:
        return styled(text, Style.YELLOW)

    def cyan(text: str) -> str:
        return styled(text, Style.CYAN)

    def magenta(text: str) -> str:
        return styled(text, Style.MAGENTA)

    # Define category colors
    category_styles = get_category_styles(green, red, yellow, cyan, blue, magenta)
    categories = get_icon_categories()

    # Check if the category exists
    available_categories = list(categories.keys())
    if category not in available_categories:
        print(f"Category '{category}' not found. Available categories:")
        for cat in available_categories:
            print(f"- {cat}")
        return

    # Display icons for the specified category
    icon_names = categories[category]
    print(f"\n{bold(category)} Icons:")

    icons_sequence = ""
    for i, name in enumerate(icon_names):
        icon = getattr(Icon, name)
        style_fn = category_styles[category][i % len(category_styles[category])]
        icons_sequence += f"{style_fn(icon)} {name}  "

        # Break into multiple lines for readability
        if (i + 1) % 4 == 0:
            icons_sequence += "\n"

    print(icons_sequence)
    print()


def get_category_styles(
    green: Callable[[str], str],
    red: Callable[[str], str],
    yellow: Callable[[str], str],
    cyan: Callable[[str], str],
    blue: Callable[[str], str],
    magenta: Callable[[str], str],
) -> dict[str, list[Callable[[str], str]]]:
    """
    Get the category styles for terminal icons.

    Args:
        green: Function to color text green
        red: Function to color text red
        yellow: Function to color text yellow
        cyan: Function to color text cyan
        blue: Function to color text blue
        magenta: Function to color text magenta

    Returns:
        Dictionary mapping category names to lists of style functions
    """
    return {
        "Status Icons": [green, red, yellow, cyan],
        "Directional": [
            blue,
            blue,
            blue,
            blue,
            blue,
            blue,
            blue,
            blue,
            blue,
            blue,
            blue,
            blue,
            green,
            green,
            green,
            green,
            green,
            green,
            green,
            green,
        ],
        "Shapes": [red, green, yellow, magenta],
        "Weather": [yellow, cyan, blue, cyan],
        "Weather Cycle": [yellow, yellow, yellow, cyan, cyan, blue, blue, magenta],
        "Globe": [green, blue, cyan],
        "Nature": [green, green],
        "Emotional": [yellow, red, green, magenta],
        "Monkeys": [yellow, yellow, yellow],
        "People": [blue, red],
        "Tech": [blue, red, green, yellow],
        "Geometric": [magenta, magenta, magenta, magenta],
        "Box Drawing - Basic": [cyan, cyan, cyan, cyan, cyan, cyan],
        "Box Drawing - Extended": [
            blue,
            blue,
            blue,
            blue,
            blue,
            blue,
            yellow,
            yellow,
            green,
            green,
            green,
            green,
        ],
        "Spinners - Braille": [
            magenta,
            magenta,
            magenta,
            magenta,
            magenta,
            magenta,
            magenta,
            magenta,
            magenta,
            magenta,
        ],
        "Spinners - Line": [cyan, cyan, cyan, cyan],
        "Spinners - Dot": [yellow, yellow, yellow, yellow, yellow, yellow, yellow, yellow],
        "Spinners - Clock": [
            cyan,
            cyan,
            cyan,
            cyan,
            cyan,
            cyan,
            cyan,
            cyan,
            cyan,
            cyan,
            cyan,
            cyan,
        ],
        "Hearts": [red, yellow, blue, magenta, green],
        "Celebration": [magenta, cyan, red, green],
    }


def get_icon_categories() -> dict[str, list[str]]:
    """
    Get the categories of terminal icons.

    Returns:
        Dictionary mapping category names to lists of icon names
    """
    return {
        "Status Icons": ["CHECK", "CROSS", "WARNING", "INFO"],
        "Directional": [
            "ARROW_RIGHT",
            "ARROW_LEFT",
            "ARROW_UP",
            "ARROW_DOWN",
            "SPIN_ARROW_1",
            "SPIN_ARROW_2",
            "SPIN_ARROW_3",
            "SPIN_ARROW_4",
            "SPIN_ARROW_5",
            "SPIN_ARROW_6",
            "SPIN_ARROW_7",
            "SPIN_ARROW_8",
            "SPIN_EMOJI_ARROW_1",
            "SPIN_EMOJI_ARROW_2",
            "SPIN_EMOJI_ARROW_3",
            "SPIN_EMOJI_ARROW_4",
            "SPIN_EMOJI_ARROW_5",
            "SPIN_EMOJI_ARROW_6",
            "SPIN_EMOJI_ARROW_7",
            "SPIN_EMOJI_ARROW_8",
        ],
        "Shapes": ["CIRCLE", "SQUARE", "TRIANGLE", "STAR"],
        "Weather": ["SUN", "CLOUD", "UMBRELLA", "SNOWFLAKE"],
        "Weather Cycle": [
            "WEATHER_SUN",
            "WEATHER_SUN_SMALL_CLOUD",
            "WEATHER_SUN_CLOUD",
            "WEATHER_CLOUD_SUN",
            "WEATHER_CLOUD",
            "WEATHER_RAIN",
            "WEATHER_SNOW",
            "WEATHER_THUNDERSTORM",
        ],
        "Globe": ["GLOBE_EUROPE_AFRICA", "GLOBE_AMERICAS", "GLOBE_ASIA_AUSTRALIA"],
        "Nature": ["TREE_EVERGREEN", "TREE_CHRISTMAS"],
        "Emotional": ["SMILE", "FROWN", "THUMBS_UP", "THUMBS_DOWN", "CLAP", "FIRE"],
        "Monkeys": ["MONKEY_SEE_NO_EVIL", "MONKEY_HEAR_NO_EVIL", "MONKEY_SPEAK_NO_EVIL"],
        "People": ["PERSON_WALKING", "PERSON_RUNNING"],
        "Tech": ["MAIL", "SCISSORS", "PENCIL", "KEY"],
        "Geometric": ["BLOCK", "LIGHT_SHADE", "MEDIUM_SHADE", "DARK_SHADE"],
        "Box Drawing - Basic": [
            "H_LINE",
            "V_LINE",
            "TOP_LEFT",
            "TOP_RIGHT",
            "BOTTOM_LEFT",
            "BOTTOM_RIGHT",
        ],
        "Box Drawing - Extended": [
            "H_LINE_HEAVY",
            "V_LINE_HEAVY",
            "TOP_LEFT_HEAVY",
            "TOP_RIGHT_HEAVY",
            "BOTTOM_LEFT_HEAVY",
            "BOTTOM_RIGHT_HEAVY",
            "BOX_CROSS",
            "BOX_CROSS_HEAVY",
            "T_RIGHT",
            "T_LEFT",
            "T_DOWN",
            "T_UP",
        ],
        "Spinners - Braille": [
            "SPIN_BRAILLE_1",
            "SPIN_BRAILLE_2",
            "SPIN_BRAILLE_3",
            "SPIN_BRAILLE_4",
            "SPIN_BRAILLE_5",
            "SPIN_BRAILLE_6",
            "SPIN_BRAILLE_7",
            "SPIN_BRAILLE_8",
            "SPIN_BRAILLE_9",
            "SPIN_BRAILLE_10",
        ],
        "Spinners - Line": ["SPIN_LINE_1", "SPIN_LINE_2", "SPIN_LINE_3", "SPIN_LINE_4"],
        "Spinners - Dot": [
            "SPIN_DOT_1",
            "SPIN_DOT_2",
            "SPIN_DOT_3",
            "SPIN_DOT_4",
            "SPIN_DOT_5",
            "SPIN_DOT_6",
            "SPIN_DOT_7",
            "SPIN_DOT_8",
        ],
        "Spinners - Clock": [
            "SPIN_CLOCK_1",
            "SPIN_CLOCK_2",
            "SPIN_CLOCK_3",
            "SPIN_CLOCK_4",
            "SPIN_CLOCK_5",
            "SPIN_CLOCK_6",
            "SPIN_CLOCK_7",
            "SPIN_CLOCK_8",
            "SPIN_CLOCK_9",
            "SPIN_CLOCK_10",
            "SPIN_CLOCK_11",
            "SPIN_CLOCK_12",
        ],
        "Hearts": ["HEART_RED", "HEART_YELLOW", "HEART_BLUE", "HEART_PURPLE", "HEART_GREEN"],
        "Celebration": ["CONFETTI", "PARTY", "BALLOON", "GIFT"],
    }
