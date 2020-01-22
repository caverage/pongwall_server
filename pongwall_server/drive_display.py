""" Drive a WS2811 Matrix using Arduino"""

import sys
import time
from typing import List

import numpy as np
import serial
from pongwall_server import pongwall_serial_protocol

# Globals
CONTROLLER = serial.Serial(sys.argv[1], 9600)

# time.sleep(5)

NUM_LEDS = 100
BYTES_PER_LED = 3


def serpentine_matrix(width: int, height: int, frame: np.ndarray) -> bytes:
    if width * height * BYTES_PER_LED != len(frame):
        raise ValueError(
            "Frame not equal to the product of the `height` and `width provided.`"
        )

    # FIXME: determine if width or height needs to go first
    frame = frame.reshape((width, height, BYTES_PER_LED))

    even_rows = frame[0::2, :]
    odd_rows = frame[1::2, ::-1]
    frame = np.empty((width, height, BYTES_PER_LED), dtype=np.uint8)
    frame[0::2] = even_rows
    frame[1::2] = odd_rows

    return bytes(frame)


def send_frame(width: int, height: int, frame: bytes):

    frame = serpentine_matrix(width, height, frame)
    packet = pongwall_serial_protocol.create_packet(frame)
    start_time = time.time()
    # for wb in packet:
    #     CONTROLLER.write(bytes([wb]))
    #
    #     while CONTROLLER.in_waiting > 0:
    #         controller_output = CONTROLLER.readline()[:-2]
    #         if controller_output == b"ACK":
    #             print("ACK recieved")
    #             break
    #         print(f"Read:  {controller_output}")
    CONTROLLER.write(packet)

    print(f"transmitted in '{round(time.time() - start_time, 4)}' seconds")
    while True:
        controller_output = CONTROLLER.readline()[:-2]
        if controller_output == b"ACK":
            print("ACK recieved")
            break
        print(f"Read:  {controller_output}")


# FRAME = bytes(sorted(np.random.bytes(NUM_LEDS * 3)))
FRAME = b"\xFF" + bytes([byte for byte in range(149)] + [byte for byte in range(150)])
FRAME = np.frombuffer(FRAME, dtype=np.uint8)
send_frame(10, 10, FRAME)
