"""
This file is provided as a sample of basic initialisation and working for
"plug-and-play" of the drivers, but is expected to be altered to implement
system control algorithms.
"""
import time
from movement import move_forward_one_cell, turn_left, turn_right, move_x_cells, turn_180
from micromouse import Micromouse
from machine import Pin

mm = Micromouse()


if __name__ == "__main__":
    mm.invert_motor_2()
    while True:
        move_forward_one_cell(mm)
        time.sleep(10)

