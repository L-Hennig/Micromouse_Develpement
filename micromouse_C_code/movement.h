/*
 * Filename: movement.h
 * Description: C++ port of movement.py + movement_speedy.py for Arduino IDE.
 *
 * movement.py's fixed 90-degree turn_left/turn_right and movement_speedy.py's
 * arbitrary-angle turn_left/turn_right(angle) are the same math with angle
 * hardcoded to 90 - merged here as overloads (turn_left(mm) just calls
 * turn_left(mm, 90)) instead of keeping two near-duplicate implementations.
 */
#ifndef MOVEMENT_H
#define MOVEMENT_H

#include "micromouse.h"

// Wheel/encoder geometry constants (from movement.py / movement_speedy.py)
const int   ENCODER_COUNT_PER_WHEEL_REV_1 = 1056;   // motor_1
const int   ENCODER_COUNT_PER_WHEEL_REV_2 = 1056;   // motor_2
const float WHEEL_DIAMETER_MM = 44.0f;
const float WHEEL_SPACING_MM  = 93.0f;
const float CELL_SIZE_MM      = 168.0f;

// Encoder counts for one cell for each wheel
const long ENCODER_COUNT_CELL_1 =
    (long)(CELL_SIZE_MM / (PI * WHEEL_DIAMETER_MM) * ENCODER_COUNT_PER_WHEEL_REV_1);
const long ENCODER_COUNT_CELL_2 =
    (long)(CELL_SIZE_MM / (PI * WHEEL_DIAMETER_MM) * ENCODER_COUNT_PER_WHEEL_REV_2);


void move_forward_one_cell(Micromouse &mm);
void move_x_cells(Micromouse &mm, int cells);

// Fixed 90-degree turns (delegate to the angle versions below)
void turn_left(Micromouse &mm);
void turn_right(Micromouse &mm);
void turn_180(Micromouse &mm);

// Arbitrary-angle turns, ported from movement_speedy.py
void turn_left(Micromouse &mm, float angle_deg);
void turn_right(Micromouse &mm, float angle_deg);

#endif
