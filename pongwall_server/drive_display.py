""" Drive a WS2811 Matrix using Arduino"""

import sys
from pathlib import Path

import imageio
import serial

from pongwall_server import frame

# Constants
CONTROLLER = serial.Serial(sys.argv[1], 115200)

MATRIX_WIDTH = 48
MATRIX_HEIGHT = 27
NUM_LEDS = MATRIX_WIDTH * MATRIX_HEIGHT
BYTES_PER_LED = 3
BYTES_PER_FRAME = NUM_LEDS * BYTES_PER_LED


def send_frame(frame_):
    CONTROLLER.write(frame_)


if __name__ == "__main__":
    IMAGE = imageio.imread(Path(sys.argv[1]))
    FRAME = frame.serpentinize(IMAGE, MATRIX_WIDTH, MATRIX_HEIGHT)
    send_frame(frame.make_data(FRAME))
