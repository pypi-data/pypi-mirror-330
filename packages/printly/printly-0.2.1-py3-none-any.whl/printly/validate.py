"""Defines functions to validate colors and font styles."""

import re
from difflib import get_close_matches
from .types import Color, FontStyle
from .const import COLORS_RGB_MAP, COMBINATOR, FONT_STYLE_CODES, HEX_PREFIX, RGB_DELIMITER

__all__ = ["validate_color", "validate_fontstyle"]

HEX_PATTERN = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def validate_color(color: Color) -> Color:
    """Validates a color to check if it is supported."""
    color = re.sub(r"(\s+|-+)", "", f"{color}").lower()
    if color is not None:
        if HEX_PREFIX in color:
            if not HEX_PATTERN.fullmatch(color):
                raise ValueError(f"Invalid HEX color '{color}'. Must be '#rgb' or '#rrggbb'")
            if len(hex_digits := color[1:]) == 3:
                hex_digits = "".join(hex_digit * 2 for hex_digit in hex_digits)
                color = f"#{hex_digits}"
        elif RGB_DELIMITER in color:
            rgb_values = color.split(RGB_DELIMITER)
            if not all((value.isdigit() for value in rgb_values)):
                raise ValueError(f"Invalid RGB color '{color}'. RGB values must be integers.")
            if not all((0 <= int(value) <= 255 for value in rgb_values)):
                raise ValueError(f"Invalid RGB color '{color}'. RGB values must be in range 0-255.")
        else:
            if color not in COLORS_RGB_MAP:
                closest = ", ".join(get_close_matches(color, COLORS_RGB_MAP, n=1))
                error_hint = f"Did you mean '{closest}'?" if closest else ""
                raise ValueError(f"Invalid color name '{color}'. {error_hint}")
    return color


def validate_fontstyle(fontstyle: FontStyle) -> FontStyle:
    """Validates a font style to check if it is supported."""
    fontstyle = re.sub(r"\s+", "", f"{fontstyle}").lower()
    fontstyles = sorted(set(fontstyle.split(COMBINATOR)))
    for fontstyle in fontstyles:
        if fontstyle not in FONT_STYLE_CODES:
            closest = ", ".join(get_close_matches(fontstyle, FONT_STYLE_CODES, n=1))
            error_hint = f"Did you mean '{closest}'?" if closest else ""
            raise ValueError(f"Invalid font style '{fontstyle}'. {error_hint}")
    return COMBINATOR.join(fontstyles)
