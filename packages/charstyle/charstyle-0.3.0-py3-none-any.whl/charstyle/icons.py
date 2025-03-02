"""
Terminal icons/emojis for charstyle.

This module provides a collection of widely supported terminal icons and emojis
that should display correctly on most modern terminals.

Most spinners have been found at:
https://raw.githubusercontent.com/sindresorhus/cli-spinners/main/spinners.json

"""

from enum import StrEnum


class Icon(StrEnum):
    """Common terminal icons/emojis that work across most modern terminals."""

    # Status icons
    CHECK = "✓"
    CROSS = "✗"
    WARNING = "⚠"
    INFO = "ℹ"

    # Directional arrows
    ARROW_RIGHT = "→"
    ARROW_LEFT = "←"
    ARROW_UP = "↑"
    ARROW_DOWN = "↓"

    # Common shapes
    CIRCLE = "●"
    SQUARE = "■"
    TRIANGLE = "▲"
    STAR = "★"

    # Weather & elements
    SUN = "☀"
    CLOUD = "☁"
    UMBRELLA = "☂"
    SNOWFLAKE = "❄"

    # Weather cycle
    WEATHER_SUN = "☀️"
    WEATHER_SUN_SMALL_CLOUD = "🌤"
    WEATHER_SUN_CLOUD = "⛅️"
    WEATHER_CLOUD_SUN = "🌥"
    WEATHER_CLOUD = "☁️"
    WEATHER_RAIN = "🌧"
    WEATHER_SNOW = "🌨"
    WEATHER_THUNDERSTORM = "⛈"

    # Globe/Earth
    GLOBE_EUROPE_AFRICA = "🌍"
    GLOBE_AMERICAS = "🌎"
    GLOBE_ASIA_AUSTRALIA = "🌏"

    # Nature
    TREE_EVERGREEN = "🌲"
    TREE_CHRISTMAS = "🎄"

    # Misc
    HEART = "♥"
    MUSIC = "♪"
    RECYCLE = "♻"
    TELEPHONE = "☎"

    # Faces
    SMILE = "☺"
    FROWN = "☹"

    # Monkeys
    MONKEY_SEE_NO_EVIL = "🙈"
    MONKEY_HEAR_NO_EVIL = "🙉"
    MONKEY_SPEAK_NO_EVIL = "🙊"

    # People
    PERSON_WALKING = "🚶"
    PERSON_RUNNING = "🏃"

    # Tech
    MAIL = "✉"
    SCISSORS = "✂"
    PENCIL = "✎"
    KEY = "⚿"

    # Geometric
    BLOCK = "█"
    LIGHT_SHADE = "░"
    MEDIUM_SHADE = "▒"
    DARK_SHADE = "▓"

    # Box drawing - basic
    H_LINE = "─"
    V_LINE = "│"
    TOP_LEFT = "┌"
    TOP_RIGHT = "┐"
    BOTTOM_LEFT = "└"
    BOTTOM_RIGHT = "┘"

    # Box drawing - extended
    H_LINE_HEAVY = "━"
    V_LINE_HEAVY = "┃"
    TOP_LEFT_HEAVY = "┏"
    TOP_RIGHT_HEAVY = "┓"
    BOTTOM_LEFT_HEAVY = "┗"
    BOTTOM_RIGHT_HEAVY = "┛"
    BOX_CROSS = "┼"
    BOX_CROSS_HEAVY = "╋"
    T_RIGHT = "├"
    T_LEFT = "┤"
    T_DOWN = "┬"
    T_UP = "┴"

    # Spinners - Braille patterns
    SPIN_BRAILLE_1 = "⠋"
    SPIN_BRAILLE_2 = "⠙"
    SPIN_BRAILLE_3 = "⠹"
    SPIN_BRAILLE_4 = "⠸"
    SPIN_BRAILLE_5 = "⠼"
    SPIN_BRAILLE_6 = "⠴"
    SPIN_BRAILLE_7 = "⠦"
    SPIN_BRAILLE_8 = "⠧"
    SPIN_BRAILLE_9 = "⠇"
    SPIN_BRAILLE_10 = "⠏"

    # Spinners - Line patterns
    SPIN_LINE_1 = "|"
    SPIN_LINE_2 = "/"
    SPIN_LINE_3 = "-"
    SPIN_LINE_4 = "\\"

    # Spinners - Dot patterns
    SPIN_DOT_1 = "⣾"
    SPIN_DOT_2 = "⣽"
    SPIN_DOT_3 = "⣻"
    SPIN_DOT_4 = "⢿"
    SPIN_DOT_5 = "⡿"
    SPIN_DOT_6 = "⣟"
    SPIN_DOT_7 = "⣯"
    SPIN_DOT_8 = "⣷"

    # Spinners - Arrow patterns
    SPIN_ARROW_1 = "←"
    SPIN_ARROW_2 = "↖"
    SPIN_ARROW_3 = "↑"
    SPIN_ARROW_4 = "↗"
    SPIN_ARROW_5 = "→"
    SPIN_ARROW_6 = "↘"
    SPIN_ARROW_7 = "↓"
    SPIN_ARROW_8 = "↙"

    # Spinners - Emoji Arrow patterns
    SPIN_EMOJI_ARROW_1 = "⬅️"
    SPIN_EMOJI_ARROW_2 = "↖️"
    SPIN_EMOJI_ARROW_3 = "⬆️"
    SPIN_EMOJI_ARROW_4 = "↗️"
    SPIN_EMOJI_ARROW_5 = "➡️"
    SPIN_EMOJI_ARROW_6 = "↘️"
    SPIN_EMOJI_ARROW_7 = "⬇️"
    SPIN_EMOJI_ARROW_8 = "↙️"

    # Spinners - Clock patterns
    SPIN_CLOCK_1 = "🕛"
    SPIN_CLOCK_2 = "🕐"
    SPIN_CLOCK_3 = "🕑"
    SPIN_CLOCK_4 = "🕒"
    SPIN_CLOCK_5 = "🕓"
    SPIN_CLOCK_6 = "🕔"
    SPIN_CLOCK_7 = "🕕"
    SPIN_CLOCK_8 = "🕖"
    SPIN_CLOCK_9 = "🕗"
    SPIN_CLOCK_10 = "🕘"
    SPIN_CLOCK_11 = "🕙"
    SPIN_CLOCK_12 = "🕚"

    # Emotional
    THUMBS_UP = "👍"
    THUMBS_DOWN = "👎"
    CLAP = "👏"
    FIRE = "🔥"

    # Hearts
    HEART_RED = "❤️"
    HEART_YELLOW = "💛"
    HEART_BLUE = "💙"
    HEART_PURPLE = "💜"
    HEART_GREEN = "💚"

    # Celebration
    CONFETTI = "🎊"
    PARTY = "🎉"
    BALLOON = "🎈"
    GIFT = "🎁"


def print_all_icons() -> None:
    """Print all available icons with their names."""
    for name, icon in [(name, icon.value) for name, icon in Icon.__members__.items()]:
        print(f"{name}: {icon}")


def get_icon(name: str) -> str:
    """
    Get an icon by its name.

    Args:
        name (str): The name of the icon to retrieve

    Returns:
        str: The icon character

    Raises:
        ValueError: If the icon name is not found
    """
    try:
        return Icon[name].value
    except KeyError as err:
        raise ValueError(
            f"Icon '{name}' not found. Available icons: {', '.join(Icon.__members__.keys())}"
        ) from err
