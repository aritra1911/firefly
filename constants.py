import numpy as np

TAU = 2 * np.pi
MAX_FLIGHT_TIME = 30
MAX_VELOCITY = 7

MEDIA_DIR = "/home/ray/codes/python/firefly/"
DEFAULT_FILENAME = "firefly"
DEFAULT_MOVIE_EXTENSION = ".mp4"

# There might be other configuration than pixel shape later...
PRODUCTION_QUALITY_CAMERA_CONFIG = {
    "pixel_height": 1440,
    "pixel_width": 2560,
    "frame_rate": 60,
}

HIGH_QUALITY_CAMERA_CONFIG = {
    "pixel_height": 1080,
    "pixel_width": 1920,
    "frame_rate": 60,
}

MEDIUM_QUALITY_CAMERA_CONFIG = {
    "pixel_height": 720,
    "pixel_width": 1280,
    "frame_rate": 30,
}

LOW_QUALITY_CAMERA_CONFIG = {
    "pixel_height": 480,
    "pixel_width": 854,
    "frame_rate": 15,
}

DEFAULT_CAMERA_CONFIG = HIGH_QUALITY_CAMERA_CONFIG

DEFAULT_PIXEL_HEIGHT = DEFAULT_CAMERA_CONFIG["pixel_height"]
DEFAULT_PIXEL_WIDTH = DEFAULT_CAMERA_CONFIG["pixel_width"]
DEFAULT_FRAME_RATE = DEFAULT_CAMERA_CONFIG["frame_rate"]

FFMPEG_BIN = "ffmpeg"
