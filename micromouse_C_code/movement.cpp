/*
 * Filename: movement.cpp
 * Description: C++ port of movement.py + movement_speedy.py for Arduino IDE.
 *
 * Turn/drive power now uses mm.speed instead of the original's hardcoded
 * 80, so navigation.cpp's explore/fast-run speed changes actually take
 * effect (previously mm.speed was set but never read anywhere).
 */
#include "movement.h"

const unsigned long MOVE_TIMEOUT_MILLISEC = 7000;   // stop moving forward if encoder count hasnt been reached after 7s.

void move_forward_one_cell(Micromouse &mm) {
  long start_1 = mm.motor_1.encoder_read();
  long start_2 = mm.motor_2.encoder_read();

  unsigned long start_time = millis(); //starts a timer 

  mm.motor_1.spin_forward(mm.speed);
  mm.motor_2.spin_forward(mm.speed);

  // Busy-polling the encoder here is fine (and fast) now that reads are
  // backed by real hardware interrupts, unlike the original MicroPython
  // soft-IRQ version this was ported from.
  while (true) {
    long count_1 = abs(mm.motor_1.encoder_read() - start_1);
    long count_2 = abs(mm.motor_2.encoder_read() - start_2);
    if (count_1 >= ENCODER_COUNT_CELL_1 || count_2 >= ENCODER_COUNT_CELL_2) break;
    if (millis() - start_time > MOVE_TIMEOUT_MILLISEC) break; //safety timeout if encoder count isnt reached after 7s due to error
  }

  mm.motor_1.spin_stop();
  mm.motor_2.spin_stop();
}

void move_x_cells(Micromouse &mm, int cells) {
  for (int i = 0; i < cells; i++) {
    move_forward_one_cell(mm);
  }
}

void turn_left(Micromouse &mm, float angle_deg) {
  long start_1 = mm.motor_1.encoder_read();
  long start_2 = mm.motor_2.encoder_read();

  // Sector of the circle traced by the wheel spacing, for the given angle.
  float turn_distance = PI * WHEEL_SPACING_MM * angle_deg / 360.0f;
  float wheel_circumference = PI * WHEEL_DIAMETER_MM;
  long turn_1 = (long)(turn_distance / wheel_circumference * ENCODER_COUNT_PER_WHEEL_REV_1);
  long turn_2 = (long)(turn_distance / wheel_circumference * ENCODER_COUNT_PER_WHEEL_REV_2);

  mm.motor_2.spin_backward(mm.speed);
  mm.motor_1.spin_forward(mm.speed);

  while (true) {
    long count_1 = abs(mm.motor_1.encoder_read() - start_1);
    long count_2 = abs(mm.motor_2.encoder_read() - start_2);
    if (count_1 >= turn_1 && count_2 >= turn_2) break;
  }

  mm.drive_stop();
}

void turn_right(Micromouse &mm, float angle_deg) {
  long start_1 = mm.motor_1.encoder_read();
  long start_2 = mm.motor_2.encoder_read();

  float turn_distance = PI * WHEEL_SPACING_MM * angle_deg / 360.0f;
  float wheel_circumference = PI * WHEEL_DIAMETER_MM;
  long turn_1 = (long)(turn_distance / wheel_circumference * ENCODER_COUNT_PER_WHEEL_REV_1);
  long turn_2 = (long)(turn_distance / wheel_circumference * ENCODER_COUNT_PER_WHEEL_REV_2);

  mm.motor_1.spin_backward(mm.speed);
  mm.motor_2.spin_forward(mm.speed);

  while (true) {
    long count_1 = abs(mm.motor_1.encoder_read() - start_1);
    long count_2 = abs(mm.motor_2.encoder_read() - start_2);
    if (count_1 >= turn_1 && count_2 >= turn_2) break;
  }

  mm.drive_stop();
}

void turn_left(Micromouse &mm) {
  turn_left(mm, 90.0f);
}

void turn_right(Micromouse &mm) {
  turn_right(mm, 90.0f);
}

void turn_180(Micromouse &mm) {
  // The original called turn_left(mm) twice; a single 180-degree turn is
  // mathematically identical since the encoder target scales linearly
  // with angle, so this does the same thing in one pass.
  turn_left(mm, 180.0f);
}
