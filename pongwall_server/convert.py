"""Python script to convert an image to the rgb values for fastled"""

import sys
from pathlib import Path

import imageio
import numpy as np

IMAGE = imageio.imread(Path(sys.argv[1]))

for row in IMAGE:
    for pixel in row:
        pixel = np.uint8(np.array(pixel[:3] * (pixel[3] / np.uint8(255))))
        print(pixel)
