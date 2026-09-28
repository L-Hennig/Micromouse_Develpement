/*
 * Filename: micromouse.ino
 * Description: C++ port of main.py for Arduino IDE (arduino-pico core).
 *
 * Two modes, switched with the RUN_MODE define below:
 *   - RUN_MODE_TEST_BRINGUP: runs a one-shot motor/encoder check in
 *     setup(), then continuously prints IR/button/ToF readings in loop().
 *     Use this while wiring up and testing each subsystem.
 *   - RUN_MODE_NAVIGATION: calls the real navigation.cpp run(mm, memory)
 *     loop - the actual competition logic.
 *
 * Swap between them by changing the single #define below - no need to
 * comment/uncomment blocks of code each time.
 */
#include "micromouse.h"
#include "memory.h"
#include "movement.h"
#include "navigation.h"

#define RUN_MODE_TEST_BRINGUP 0
#define RUN_MODE_NAVIGATION   1

#define RUN_MODE RUN_MODE_TEST_BRINGUP   // <-- change this line to switch modes

#define TEST_LOOP_ALL             0   // IR + ToF + buttons (the slower one)
#define TEST_LOOP_ENCODERS_ONLY   1   // just encoders, fast

#define TEST_LOOP_MODE TEST_LOOP_ENCODERS_ONLY   // <-- change this to switch what the live loop prints

Micromouse mm;
Memory memory;

// --- Bring-up test -------------------------------------------------------

static void print_encoders(const char *label) {
  Micromouse::Encoders e = mm.get_encoders();
  Serial.print(label);
  Serial.print(": encoder_1 = ");
  Serial.print(e.encoder_1);
  Serial.print(", encoder_2 = ");
  Serial.println(e.encoder_2);
}

// One-shot checks: drive forward, then drive forward again with motors
// inverted (should visibly reverse direction if wiring/invert logic is
// correct), printing encoder counts after each so you can see them
// actually counting.

static void bringup_test_setup() {


  ///////////////////////////////////////////////////////////

  // Serial.println("=== Movement test ===");

  // for (int i = 0; i < 3; i++) {
  //   move_forward_one_cell(mm);
  //   delay(1000);
  // }

  // turn_left(mm);
  // delay(1000);

  // move_forward_one_cell(mm);
  // mm.drive_stop();

  // print_encoders("Finished");

  //////////////////////////////////////////////////////

  // Serial.println("=== Micromouse bring-up test ===");

  // Serial.println("Driving forward for 1s...");
  // //mm.drive_forward(255);
  // delay(1000);
  // mm.drive_stop();
  // print_encoders("After forward");

  // Serial.println("Inverting both motors, driving 'forward' again for 1s...");
  // Serial.println("(the mouse should now visibly move the OPPOSITE way)");
  // mm.invert_motor_1();
  // mm.invert_motor_2();
  // //mm.drive_forward(255);
  // delay(1000);
  // print_encoders("After inverted forward");

  // // Revert the inversion so motors are back to their normal orientation
  // // for anything that runs after this test (e.g. switching to
  // // RUN_MODE_NAVIGATION later).
  // mm.invert_motor_1();
  // mm.invert_motor_2();

  // Serial.println("=== One-shot test done - now printing live sensor readings ===");
}

// Runs continuously - what it prints depends on TEST_LOOP_MODE above.
static void bringup_test_loop() {
#if TEST_LOOP_MODE == TEST_LOOP_ENCODERS_ONLY
  float front = mm.get_tof_distance(1);
  float left  = mm.get_tof_distance(2);
  float right = mm.get_tof_distance(3);

  Serial.print("ToF front/left/right (mm): ");
  Serial.print(front); Serial.print(" / ");
  Serial.print(left);  Serial.print(" / ");
  Serial.println(right);

  delay(100);

#else   // TEST_LOOP_ALL
  Micromouse::IrReadings ir = mm.get_ir_values();
  float front = mm.get_tof_distance(1);
  float left  = mm.get_tof_distance(2);
  float right = mm.get_tof_distance(3);
  bool btn1 = mm.get_button(1);
  bool btn2 = mm.get_button(2);

  Serial.print("IR[1,2,3]=");
  Serial.print(ir.ir_1); Serial.print(",");
  Serial.print(ir.ir_2); Serial.print(",");
  Serial.print(ir.ir_3);

  Serial.print("  ToF front/left/right (mm) = ");
  Serial.print(front); Serial.print(" / ");
  Serial.print(left);  Serial.print(" / ");
  Serial.print(right);

  Serial.print("  BTN1=");
  Serial.print(btn1);
  Serial.print(" BTN2=");
  Serial.println(btn2);

  delay(300);
#endif
}

// --- Arduino entry points --------------------------------------------

void setup() {
  Serial.begin(115200);
  mm.begin();

#if RUN_MODE == RUN_MODE_NAVIGATION
  // run() contains its own infinite loop and never returns, so it
  // belongs in setup(), not loop().
  run(mm, memory);
#else
  bringup_test_setup();
#endif
}

void loop() {
#if RUN_MODE == RUN_MODE_NAVIGATION
  // Intentionally empty - run() above never returns.
#else
  bringup_test_loop();
#endif
}
