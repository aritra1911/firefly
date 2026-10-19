import cairo
import numpy as np

from constants import *
from movie_writer import MovieWriter
from utils import *


class Firefly:
    def __init__(self, position):
        self.set_position(position)
        self.set_velocity(np.zeros(2))
        self.set_target(np.zeros(2))
        self.set_acceleration(np.zeros(2))
        self.set_flight_time(0.0)
        self.clear_elapsed_time()
        self.radius = DEFAULT_GLOW_RADIUS
        self.change_color()
        self.in_flight = False

    def __repr__(self):
        return f"position={self.position}, accleration={self.acceleration}, velocity={self.velocity}, in_flight={self.in_flight}"

    def get_position(self):
        return self.position

    def get_velocity(self):
        return self.velocity

    def get_target(self):
        return self.target

    def get_acceleration(self):
        return self.acceleration

    def get_radius(self):
        return self.radius

    def get_color(self):
        return self.color

    def flying(self):
        return self.in_flight

    def set_flying(self):
        self.in_flight = True

    def set_velocity(self, velocity):
        self.velocity = velocity

    def set_target(self, target):
        self.target = target

    def set_radius(self, radius):
        self.radius = radius

    def set_position(self, position):
        self.position = position

    def set_flight_time(self, time):
        self.flight_time = time

    def set_elapsed_time(self, time):
        self.elapsed_time = time

    def clear_elapsed_time(self):
        self.set_elapsed_time(0.0)

    def increment_elapsed_time(self, dt):
        self.elapsed_time += dt

        # If firefly has completed her current journey set her to not
        # flying until sim gives her a new target.
        if self.elapsed_time >= self.flight_time:
            self.in_flight = False
            self.clear_elapsed_time()

    def set_acceleration(self, vector):
        self.acceleration = vector

    def update_acceleration(self):
        delta_v = self.target - self.velocity
        remaining_time = self.flight_time - self.elapsed_time
        self.acceleration = delta_v / remaining_time

    def update_velocity(self, dv):
        self.velocity += dv

    def nudge(self, dt):
        self.set_position(self.position + self.velocity * dt)

    def angle_diff(self, target):
        return np.fabs(np.angle(target) - np.angle(self.velocity))

    def change_color(self):
        self.color = get_random_color()


class Firefield:
    def __init__(self, population):
        self.pixel_width = DEFAULT_PIXEL_WIDTH
        self.pixel_height = DEFAULT_PIXEL_HEIGHT
        self.frame_rate = DEFAULT_FRAME_RATE
        self.pixel_array_dtype = "uint8"
        self.n_channels = 4
        self.pattern = {
            "background": cairo.SolidPattern(0, 0, 0),
            "foreground": cairo.SolidPattern(1, 1, 1),
        }
        self.writer = MovieWriter(self.pixel_width, self.pixel_height, self.frame_rate)
        self.fireflies: list[Firefly] = []
        self.max_magnitude = MAX_VELOCITY
        self.population = population
        self.dimensions = self.get_dimensions()
        self.sim_dt = DEFAULT_SIM_TIMESTEP
        self.render_dt = 1.0 / self.frame_rate
        self.init_field()

    def get_dimensions(self) -> float:
        aspect_ratio = self.pixel_width / self.pixel_height
        if aspect_ratio >= 1.0:
            return np.array([aspect_ratio, 1])
        return np.array(np.array[1, aspect_ratio])

    def create_new_firefly(self):
        self.fireflies.append(
            Firefly(
                get_random_position(
                    dimensions=self.dimensions,
                    boundary=0.1,
                )
            )
        )

    def init_field(self):
        self.pixel_array = np.zeros(
            (self.pixel_width, self.pixel_height, self.n_channels),
            dtype=self.pixel_array_dtype,
        )

        self.surface = cairo.ImageSurface.create_for_data(
            self.pixel_array, cairo.FORMAT_ARGB32, self.pixel_width, self.pixel_height
        )
        self.ctx = cairo.Context(self.surface)

        # Normalizing the canvas
        self.ctx.scale(self.pixel_height, self.pixel_height)
        self.paint_it_black()
        self.populate_field()

    def paint_it_black(self):
        self.ctx.set_source(self.pattern["background"])
        self.ctx.paint()

    def draw_vector(self, position, vector, color, magnitude=0.1):
        # If null vector supplied, don't draw anything.
        if not np.any(vector):
            return

        xc, yc = position
        v = magnitude * (vector / np.linalg.norm(vector))
        # v = magnitude * vector
        self.ctx.move_to(xc, yc)
        self.ctx.line_to(xc + v[0], yc + v[1])
        self.ctx.close_path()
        self.ctx.set_source_rgb(*hex_to_rgb(color))  # Solid color
        self.ctx.set_line_width(0.002)
        self.ctx.stroke()

    def draw_firefly(self, firefly, pattern):
        xc, yc = firefly.get_position()
        self.ctx.set_source(pattern)
        self.ctx.arc(xc, yc, firefly.get_radius(), 0, TAU)
        self.ctx.fill()

    def draw_fireflies(self):
        for firefly in self.fireflies:
            self.draw_firefly(
                firefly=firefly,
                pattern=cairo.SolidPattern(*hex_to_rgb(firefly.get_color())),
            )
            # Draw some vectors for debugging
            # self.draw_vector(firefly.get_position(), firefly.get_velocity(), BLUE)
            # self.draw_vector(firefly.get_position(), firefly.get_target(), GREEN)
            # self.draw_vector(firefly.get_position(), firefly.get_acceleration(), RED)

    def populate_field(self):
        for _ in range(self.population):
            self.create_new_firefly()

    def begin_animation(self, time):
        total_frames = time * self.frame_rate
        written_frames = 0
        self.writer.open_movie_pipe()
        while written_frames < total_frames:
            self.paint_it_black()
            self.fly(is_last_frame=written_frames == total_frames - 1)
            self.writer.write_frame(self.pixel_array)
            written_frames += 1
            print(str((written_frames / total_frames) * 100) + " %", end="\r")
        self.writer.close_movie_pipe()

    def fly(self, is_last_frame: bool):
        # Draw the Fireflies for this frame.
        self.draw_fireflies()

        # If we just drew for the last frame, we don't need to perform
        # the next simulation since that won't make it into the movie.
        if is_last_frame:
            return

        # Simulate flying incrementing by sim_dt timesteps until it is
        # time to render the next the frame.
        time_since_last_frame = 0.0
        while time_since_last_frame < self.render_dt:
            for firefly in self.fireflies:
                if not firefly.flying():
                    firefly.set_flight_time(get_random_flight_time())
                    firefly.set_target(get_random_vector(self.max_magnitude))
                    firefly.update_acceleration()
                    firefly.change_color()
                    firefly.set_flying()
                    continue

                # Calculate vector field at current position
                field_retardation = get_field_retardation(
                    position=firefly.get_position(), field_dimensions=self.dimensions
                )

                # Update firefly for current dt
                net_acceleration = firefly.get_acceleration() + field_retardation
                firefly.update_velocity(dv=net_acceleration * self.sim_dt)
                firefly.nudge(self.sim_dt)
                firefly.update_acceleration()

                # Rectify firefly position if she has moved out of the
                # field.  This essentially imitates a donut shaped
                # field.
                position = firefly.get_position()
                firefly.set_position(position % self.dimensions)

                firefly.increment_elapsed_time(self.sim_dt)

            time_since_last_frame += self.sim_dt


def main():
    field = Firefield(100)
    field.begin_animation(300)


if __name__ == "__main__":
    main()
