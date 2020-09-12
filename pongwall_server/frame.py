"""Python script to convert an image to the rgb values for fastled"""

import sys
from array import array

import imageio
import numpy as np


def serpentinize(raw_frame: imageio.core.util.Array, width, height):
    # FIXME: determine if width or height needs to go first
    even_rows = raw_frame[0::2, :]
    odd_rows = raw_frame[1::2, ::-1]
    frame = np.empty((width, height), dtype=np.uint8)
    frame[0::2] = even_rows
    frame[1::2] = odd_rows

    return frame


def make_data(frame: np.ndarray):
    frame_data = array("B")
    for row in frame:
        for pixel in row:
            # FIXME: this should be better
            # right now, we strip off the opacity (because it's not part of the data)
            # and we multiply the percentage opacity against the brightness of the pixel
            pixel = np.uint8(np.array(pixel[:3] * (pixel[3] / np.uint8(255))))
            frame_data.append(*pixel)
    print(type(frame_data))
    return frame_data
