import subprocess
from constants import *

class MovieWriter:
    def __init__(self, width, height, frame_rate):
        width = width
        height = height
        fps = frame_rate
        movie_file_extension = DEFAULT_MOVIE_EXTENSION
        file_path = MEDIA_DIR + DEFAULT_FILENAME + DEFAULT_MOVIE_EXTENSION

        self.command = [
            FFMPEG_BIN,
            '-y',  # overwrite output file if it exists
            '-f', 'rawvideo',
            '-s', '%dx%d' % (width, height),  # size of one frame
            '-pix_fmt', 'bgra',
            '-r', str(fps),  # frames per second
            '-i', '-',  # The imput comes from a pipe
            '-c:v', 'h264_nvenc',
            '-an',  # Tells FFMPEG not to expect any audio
            '-loglevel', 'error',
        ]
        if movie_file_extension == ".mov":
            # This is if the background of the exported video
            # should be transparent.
            self.command += [
                '-vcodec', 'qtrle',
                # '-vcodec', 'png',
            ]
        else:
            self.command += [
                '-vcodec', 'libx264',
                '-pix_fmt', 'yuv420p',
            ]
        self.command += [file_path]

    def open_movie_pipe(self):
        self.writing_process = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE
        )

    def write_frame(self, frame):
        self.writing_process.stdin.write(frame.tostring())

    def close_movie_pipe(self):
        self.writing_process.stdin.close()
