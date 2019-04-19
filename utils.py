import numpy as np
import random
from constants import TAU, MAX_FLIGHT_TIME

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
