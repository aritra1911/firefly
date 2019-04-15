import numpy as np
import cairo
from constants import *
from movie_writer import MovieWriter
from utils import *


class Firefly():
    def __init__(self, position, pixel_width, pixel_height):
        self.set_position(position, pixel_width, pixel_height)
        self.set_velocity(np.zeros(2))
        self.reset()

    def reset(self):
        self.acceleration = np.zeros(2)
        self.set_flight_time(0)
        self.set_dt(0)
        self.in_flight = False
        self.elapsed_time = 0

    def get_position(self):
        return self.position

    def get_velocity(self):
        return self.velocity

    def get_acceleration(self, target, run_time):
        return (target - self.velocity) / run_time

    def flying(self):
        return self.in_flight

    def set_flying(self):
        self.in_flight = True

    def set_velocity(self, velocity):
        self.velocity = velocity

    def set_target(self, target):
        self.target = target

    def init_acceleration(self):
        self.acceleration = (self.target - self.velocity) / self.flight_time

    def set_position(self, position, pixel_width, pixel_height):
        self.position = position
        self.position %= np.array([
            pixel_width,
            pixel_height
        ])

    def set_flight_time(self, time):
        self.flight_time = time

    def set_dt(self, dt):
        self.dt = dt

    def calculate_dt(self, frame_rate):
        self.dt = self.flight_time / frame_rate

    def increment_elapsed_time(self):
        self.elapsed_time += self.dt
        if self.elapsed_time >= self.flight_time:
            return False
        return True

    def update_velocity(self):
        self.velocity += self.acceleration * self.dt

    def update_position(self, pixel_width, pixel_height):
        self.set_position(
            self.position + self.velocity,
            pixel_width, pixel_height
        )

    def angle_diff(self, target):
        return np.fabs(np.angle(target) - np.angle(self.velocity))

    def move(self, pixel_width, pixel_height):
        # dt = run_time / self.frame_rate * run_time
        self.update_velocity()
        self.update_position(pixel_width, pixel_height)


class Firefield:
    def __init__(self, population):
        self.pixel_width = DEFAULT_PIXEL_WIDTH
        self.pixel_height = DEFAULT_PIXEL_HEIGHT
        self.frame_rate = DEFAULT_FRAME_RATE
        self.pixel_array_dtype = 'uint8'
        self.n_channels = 4
        self.pattern = {
            "background" : cairo.SolidPattern(0, 0, 0),
            "foreground" : cairo.SolidPattern(1, 1, 1)
        }
        self.writer = MovieWriter(
            self.pixel_width, self.pixel_height, self.frame_rate
        )
        self.fireflies = list()
        self.max_magnitude = MAX_VELOCITY
        self.population = population
        self.init_field()

    def create_new_firefly(self):
        self.fireflies.append(Firefly(
            get_random_position(self.pixel_width, self.pixel_height),
            self.pixel_width, self.pixel_height
        ))

    def init_field(self):
        self.pixel_array = np.zeros(
            (self.pixel_width, self.pixel_height, self.n_channels),
            dtype=self.pixel_array_dtype
        )

        self.surface = cairo.ImageSurface.create_for_data(
            self.pixel_array,
            cairo.FORMAT_ARGB32,
            self.pixel_width, self.pixel_height
        )
        self.ctx = cairo.Context(self.surface)

        # Normalizing the canvas
        # self.ctx.scale(
        #     self.pixel_width,
        #     self.pixel_height
        # )
        self.paint_it_black()
        self.populate_field()

    def paint_it_black(self):
        self.ctx.set_source(self.pattern["background"])
        self.ctx.paint()

    def draw_firefly(self, firefly, pattern):
        xc, yc = firefly.get_position()
        radius = 3
        self.ctx.set_source(pattern)
        self.ctx.arc(xc, yc, radius, 0, TAU)
        self.ctx.fill()

    def populate_field(self):
        for _ in range(self.population):
            self.create_new_firefly()

    def begin_animation(self, time):
        elapsed_time = 0
        self.writer.open_movie_pipe()
        while elapsed_time < time:
            self.paint_it_black()
            self.fly()
            self.writer.write_frame(self.pixel_array)
            elapsed_time += 1 / self.frame_rate
            print(str((elapsed_time / time) * 100) + " %", end='\r')
        self.writer.close_movie_pipe()

    def fly(self):
        for firefly in self.fireflies:
            if not firefly.flying():
                firefly.set_flight_time(get_random_flight_time())
                firefly.calculate_dt(self.frame_rate)
                firefly.set_target(get_random_vector(self.max_magnitude))
                firefly.init_acceleration()
                firefly.set_flying()
            firefly.move(self.pixel_width, self.pixel_height)
            self.draw_firefly(firefly, self.pattern["foreground"])
            if not firefly.increment_elapsed_time():
                firefly.reset()


def main():
    field = Firefield(500)
    field.begin_animation(60)

if __name__ == '__main__':
    main()