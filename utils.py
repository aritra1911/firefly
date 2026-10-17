import random

import numpy as np

from constants import MAX_FLIGHT_TIME, PALETTE, TAU


def get_random_vector(max):
    magnitude = random.uniform(0, max)
    direction = random.uniform(0, TAU)
    return get_vector(magnitude, direction)


def get_vector(magnitude, direction):
    return magnitude * np.array([np.cos(direction), np.sin(direction)])


def get_random_position(dimensions, boundary):
    return np.random.uniform(dimensions * boundary, dimensions * (1 - boundary))


def get_random_flight_time():
    return random.uniform(0, MAX_FLIGHT_TIME)


def hex_to_rgb(color_code):
    if not isinstance(color_code, str):
        raise TypeError("Color code must be a string")

    if not color_code.startswith("#") or len(color_code) != 7:
        raise ValueError(
            "Color codes must start with '#' and must be 7 characters long"
        )

    return [int(color_code[i : i + 2], 16) / 255 for i in range(1, 7, 2)]


def get_random_color():
    return random.choice(PALETTE)


def get_retardation(x, edge):
    k = 1.0e-3  # Constant
    mid = edge / 2.0
    magnitude = k / (x**2.0 * (edge - x) ** 2.0)
    return magnitude if x < mid else -magnitude


def get_field_retardation(position, field_dimensions):
    x, y = position
    w, h = field_dimensions
    return np.array(
        [
            get_retardation(x, w),
            get_retardation(y, h),
        ]
    )
