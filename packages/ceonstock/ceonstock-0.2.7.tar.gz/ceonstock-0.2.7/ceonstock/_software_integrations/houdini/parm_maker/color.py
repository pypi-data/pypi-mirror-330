# Helper functions for working with color
from typing import Tuple


# TODO parse hex string to produce value
def color_hex_to_rgb(hex_value: str) -> Tuple[int, int, int]:
    """Convert from a hexstring to a list of floats in the 0-1 range"""
    hex_value = hex_value.lstrip("#")
    # print(f"Got hex color: {hex_value}")
    if len(hex_value) == 3:
        # If we receive a 3-char hex string, double it to accurately represent the full hex col
        # E.g. #F6B Should become #FF66BB
        hex_value = "".join([char * 2 for char in hex_value])
    # print(f"Processing hex color: {hex_value}")
    # Slice the string into groups of 2 chars and convert to int.
    rgb = tuple(int(hex_value[i : i + 2], 16) for i in (0, 2, 4))
    # TODO rgba version (in a separate function)
    # rgba = tuple(int(hex_value[i : i + 2], 16) for i in (0, 2, 4, 6))
    return rgb


def color_hex_to_hou(hex_value: str) -> Tuple[float, float, float]:
    rgb_color = color_hex_to_rgb(hex_value)
    normalized_color = tuple([rgb_to_normalized(val) for val in rgb_color])
    return normalized_color


def rgb_to_normalized(rgb_value: int) -> float:
    """Convert from 0-255(int) to 0-1(float)"""
    normalized_value = rgb_value / 255.0
    return normalized_value


def normalized_to_rgb(normalized_value: float) -> int:
    """Convert from 0-1 (float) to 0-255 (int)"""
    rgb_value = round(normalized_value * 255)
    return rgb_value
