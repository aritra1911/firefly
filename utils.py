import numpy as np
import random
from constants import TAU, MAX_FLIGHT_TIME, PALETTE

def get_random_vector(max):
    magnitude = random.uniform(0, max)
    direction = random.uniform(0, TAU)
    return get_vector(magnitude, direction)

def get_vector(magnitude, direction):
    return magnitude * np.array([
        np.cos(direction),
        np.sin(direction)
    ])

def get_random_position(pixel_width, pixel_height):
    return np.array([
        random.uniform(0, pixel_width),
        random.uniform(0, pixel_height)
    ])

def get_random_flight_time():
    return random.uniform(0, MAX_FLIGHT_TIME)

def hex_to_rgb(color_code):
    if not isinstance(color_code, str):
        raise TypeError("Color code must be a string")

    if not color_code.startswith("#") or len(color_code) != 7:
        raise ValueError(
            "Color codes must start with '#' and must be 7 characters long"
        )

    return [
        int(color_code[i:i+2], 16) / 255
        for i in range(1, 7, 2)
    ]

def get_random_color():
    return random.choice(PALETTE)
