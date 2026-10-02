/*
 * Filename: navigation.cpp
 * Description: C++ port of navigation.py for Arduino IDE (arduino-pico core).
 */
#include "navigation.h"
#include "movement.h"

static bool wait_for_release(Micromouse &mm, uint8_t button_num) {
  while (mm.get_button(button_num)) {
    delay(10);
  }
  return true;
}

enum PressType { PRESS_SINGLE, PRESS_DOUBLE };

// Blocks until a press is detected, then determines single vs. double.
static PressType classify_press(Micromouse &mm, uint8_t button_num) {
  wait_for_release(mm, button_num);
  unsigned long start = millis();
  while (millis() - start < DOUBLE_PRESS_WINDOW_MS) {
    if (mm.get_button(button_num)) {
      wait_for_release(mm, button_num);
      return PRESS_DOUBLE;
    }
    delay(10);
  }
  return PRESS_SINGLE;
}

void read_walls(Micromouse &mm, Memory &memory) {
  float front = mm.get_tof_distance(1);
  float left  = mm.get_tof_distance(2);
  float right = mm.get_tof_distance(3);

  Direction front_dir = ALL_DIRECTIONS[mm.heading % 4];
  Direction left_dir  = ALL_DIRECTIONS[((mm.heading - 1) % 4 + 4) % 4];
  Direction right_dir = ALL_DIRECTIONS[(mm.heading + 1) % 4];

  if (front >= 20 && front <= 120) memory.set_wall(mm.x, mm.y, front_dir);
  if (left  >= 20 && left  <= 120) memory.set_wall(mm.x, mm.y, left_dir);
  if (right >= 20 && right <= 120) memory.set_wall(mm.x, mm.y, right_dir);
}

void move_to_next_cell(Micromouse &mm, Direction next_dir) {
  int dif = mm.heading - next_dir;
  if (dif == 0) {
    // already facing the right way
  } else if (dif == 1 || dif == -3) {
    turn_left(mm);
  } else if (dif == 2 || dif == -2) {
    turn_180(mm);
  } else if (dif == 3 || dif == -1) {
    turn_right(mm);
  }
  // The Python version never updated mm.heading or mm.x/mm.y here - added
  // this so explore/fast-run actually track where the mouse is. Heading
  // is set to the direction just turned to (clockwise N,E,S,W = 0,1,2,3),
  // then x/y step one cell in that direction using the same step_cell()
  // flood_fill.cpp uses internally, so both stay in exact agreement.
  mm.heading = next_dir;
  move_forward_one_cell(mm);

  Cell moved_to = step_cell(mm.x, mm.y, static_cast<Direction>(mm.heading));
  mm.x = moved_to.x;
  mm.y = moved_to.y;
}

void explore_step(Micromouse &mm, Memory &memory,
                  const Cell *goal_cells, uint8_t goal_count) {

  if (!memory.is_visited(mm.x, mm.y)) {
    read_walls(mm, memory);
    memory.mark_visited(mm.x, mm.y);
  }
  update_flood(memory, goal_cells, goal_count);
  Direction next_dir = get_next_move(memory, mm.x, mm.y);
  if (next_dir == DIR_NONE) {
    return;
  }
  move_to_next_cell(mm, next_dir);
}


bool fast_run(Micromouse &mm, Memory &memory) {
  const Cell *goal_cells = mm.center_cells;
  uint8_t goal_count = mm.center_cells_count;

  memory.block_unvisited();
  update_flood(memory, goal_cells, goal_count);

  Direction path[MAX_PATH_LEN];
  int path_len = get_full_path(memory, mm.start_cell, goal_cells, goal_count, path);
  if (path_len < 0) {
    return false;   // stuck - goal unreachable (Python raised RuntimeError)
  }

  for (int i = 0; i < path_len; i++) {
    move_to_next_cell(mm, path[i]);
  }
  return true;
}

void run_explore_leg(Micromouse &mm, Memory &memory, const Cell *goal_cells, uint8_t goal_count) {
  while (!is_solved(memory, mm.x, mm.y)) {
    if (mm.get_button(1)) {
      mm.drive_stop();
      mm.x = mm.start_cell.x;
      mm.y = mm.start_cell.y;
      mm.heading = NORTH;
      return;
    }
    explore_step(mm, memory, goal_cells, goal_count);
  }
}

Action wait_for_next_action(Micromouse &mm) {
  while (true) {
    if (mm.get_button(1)) {
      if (classify_press(mm, 1) == PRESS_DOUBLE) {
        return ACTION_FULL_RESET;
      }
      return ACTION_START_RUN;
    }
    if (mm.get_button(2)) {
      if (classify_press(mm, 2) == PRESS_DOUBLE) {
        return ACTION_FORCE_FAST;
      }
      // single press of button 2 does nothing, matching the Python version
    }
    delay(10);
  }
}

static void full_reset(Micromouse &mm, Memory &memory,
                        int &explore_count, int &fast_count, bool &mode_is_fast) {
  memory.reset();
  mm.x = mm.start_cell.x;
  mm.y = mm.start_cell.y;
  mm.heading = NORTH;
  // removed line because otherwise walls not read in starting cell: memory.mark_visited(mm.x, mm.y);
  explore_count = 0;
  fast_count = 0;
  mode_is_fast = false;
}

void run(Micromouse &mm, Memory &memory) {
  int explore_count, fast_count;
  bool mode_is_fast;
  full_reset(mm, memory, explore_count, fast_count, mode_is_fast);

  while (true) {
    Action action = wait_for_next_action(mm);

    if (action == ACTION_FULL_RESET) {
      full_reset(mm, memory, explore_count, fast_count, mode_is_fast);
      continue;
    }
    if (action == ACTION_FORCE_FAST) {
      mode_is_fast = true;
      continue;
    }

    if (!mode_is_fast) {
      int speed_index = (explore_count < 3) ? explore_count : 2;
      mm.speed = EXPLORE_SPEEDS[speed_index];

      run_explore_leg(mm, memory, mm.center_cells, mm.center_cells_count);

      if (is_solved(memory, mm.x, mm.y)) {
        delay(2000);
        Cell return_goal[1] = { mm.start_cell };
        run_explore_leg(mm, memory, return_goal, 1);
      }

      explore_count++;
      if (explore_count >= 3) {
        mode_is_fast = true;
      }
    } else {
      mm.speed = (fast_count == 0) ? FAST_SPEED_FIRST : FAST_SPEED_DEFAULT;

      if (!fast_run(mm, memory)) {
        mm.led_red_set(true);
        continue;
      }

      fast_count++;
    }
  }
}
