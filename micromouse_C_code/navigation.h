/*
 * Filename: navigation.h
 * Description: C++ port of navigation.py for Arduino IDE (arduino-pico core).
 *
 * Notable differences from the Python version:
 *   - mm.start_cells (plural, used in fast_run) was a typo for the
 *     singular mm.start_cell that Micromouse actually defines - used
 *     start_cell here, since get_full_path only ever takes one start cell.
 *   - Python's RuntimeError (raised by get_full_path when the goal is
 *     unreachable) is replaced with a bool/int return code, since
 *     exceptions aren't idiomatic for embedded C++.
 *   - The Python version's move_to_next_cell() never updated mm.heading
 *     or mm.x/mm.y after turning and moving - added here so explore and
 *     fast-run actually track where the mouse is (heading is clockwise:
 *     N,E,S,W = 0,1,2,3).
 *   - read_walls() will be a no-op until Micromouse::get_tof_distance()
 *     is wired up to the real driver (currently a stub - see micromouse.h).
 */
#ifndef NAVIGATION_H
#define NAVIGATION_H

#include "micromouse.h"
#include "memory.h"
#include "flood_fill.h"

const unsigned long DOUBLE_PRESS_WINDOW_MS = 2000;
const int EXPLORE_SPEEDS[3] = { 128, 153, 178 };
const int FAST_SPEED_FIRST = 230;
const int FAST_SPEED_DEFAULT = 255;

void read_walls(Micromouse &mm, Memory &memory);
void move_to_next_cell(Micromouse &mm, Direction next_dir);
void explore_step(Micromouse &mm, Memory &memory, const Cell *goal_cells, uint8_t goal_count);

// Returns false if the run got stuck (goal unreachable) - see header note
// above about replacing Python's RuntimeError.
bool fast_run(Micromouse &mm, Memory &memory);

// Runs explore_step until solved or aborted via button 1. Always returns
// after one or the other.
void run_explore_leg(Micromouse &mm, Memory &memory, const Cell *goal_cells, uint8_t goal_count);

enum Action { ACTION_FULL_RESET, ACTION_START_RUN, ACTION_FORCE_FAST };
Action wait_for_next_action(Micromouse &mm);

// Main control loop - does not return (matches the Python `while True`).
// Call this from loop(), or just call it once from setup() since it never
// returns on its own.
void run(Micromouse &mm, Memory &memory);

#endif