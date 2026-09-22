import time
from memory import Memory, N, E, S, W
from flood_fill import update_flood, get_next_move, is_solved, get_full_path
from movement import move_forward_one_cell, turn_left, turn_right, move_x_cells, turn_180

DOUBLE_PRESS_WINDOW_MS = 2000
FAST_RUN_TIMEOUT_MS = 6 * 60 * 1000
EXPLORE_SPEEDS = [128, 153, 178]
FAST_SPEED_FIRST = 230
FAST_SPEED_DEFAULT = 255

# read walls
def read_walls(mm, memory):
    """
    Reads TOF sensors to test if there is a wall in front, left or right and
    updates memory

    Parameters:

    """
    front = mm.get_tof_distance(1)
    left = mm.get_tof_distance(2)
    right = mm.get_tof_distance(3)

    directions = [N, E, S, W] 

    front_dir = directions[mm.heading % 4]
    left_dir = directions[(mm.heading - 1) % 4]
    right_dir = directions[(mm.heading + 1) % 4]

    if (20 <= front <= 120):
        memory.set_wall(mm.x, mm.y, front_dir)
    if (20 <= left <= 120):
        memory.set_wall(mm.x, mm.y, left_dir)
    if (20 <= right <= 120):
        memory.set_wall(mm.x, mm.y, right_dir)
    return

def move_to_next_cell(mm, next_dir):
    # move to next cell
    dif = int(mm.heading - next_dir)

    if dif == 0:
        pass
    elif dif == 1 or dif == -3:
        turn_left(mm)
    elif dif == 2 or dif == -2:
        turn_180(mm)
    elif dif == 3 or dif == -1:
        turn_right(mm)
    else:
        raise ValueError("heading and next_dir but be between 0 and 3 inclusive!")

    move_forward_one_cell(mm)

# Explore step
def explore_step(mm, memory, goal_cells):
    # read walls if unvisited
    if not memory.is_visited(mm.x, mm.y):
        read_walls(mm, memory)

    # update floodfill
    update_flood(memory, goal_cells)

    # get next move returns the dirction
    next_dir = get_next_move(memory, mm.x, mm.y)

    move_to_next_cell(mm, next_dir)

    # update visited memory 
    # Could change to only do if not visisted
    memory.mark_visited(mm.x, mm.y)

    return

# fast run
def fast_run(mm, memory):
    goal_cells = (mm.center_x, mm.center_y)

    # block all walls in unvisited cells
    memory.block_unvisited()
    update_flood(memory, goal_cells)

    # calc path
    path = get_full_path(memory, (mm.start_x, mm.start_y), goal_cells)

    # follow path
    for direction in path:
        move_to_next_cell(mm, direction)
        pass
    return


def _wait_for_release(mm, button_num):
    while mm.get_button(button_num):
        time.sleep_ms(10)

def _clasiffy_press(mm, button_num):
    """Blocks until a press is detected, then determines single vs double"""
    _wait_for_release(mm, button_num)
    start = time.tick_ms()
    while time.ticks_diff(time.tick_ms(), start) < DOUBLE_PRESS_WINDOW_MS:
        if mm.get_button(button_num):
            _wait_for_release(mm, button_num)
            return "double"
        time.sleep_ms(10)
    return "single"

def wait_for_next_action(mm):
    """"""
    while True:
        if mm.get_button(1):
            if _clasiffy_press(mm, 1) == "double":
                return "full_reset"
            else: 
                return "start_run"

        if mm.get_button(2):
            if _clasiffy_press(mm, 2) == "double":
                return "force_fast"
        time.sleep_ms(10)


def run_explore_leg(mm, memory, goal_cells):
    """Runs until solved or aborted via BTN1. Always returns after one or the other."""
    while not is_solved(memory, mm.x, mm.y):
        if mm.get_button(1):
            mm.drive_stop()
            mm.x, mm.y = mm.start_cell
            mm.heading = N
            return
        explore_step(mm, memory, goal_cells)




# Main Control Loop
def run(mm, memory):
    def full_reset():
        memory.reset()
        mm.x, mm.y = mm.start_cell
        mm.heading = N
        memory.mark_visited(mm.x, mm.y)
        return 0, 0, "explore", time.ticks_ms()

    explore_count, fast_count, mode, reset_time = full_reset()

    while True:
        action = wait_for_next_action(mm)

        if action == "full_reset":
            explore_count, fast_count, mode, reset_time = full_reset()
            continue

        if action == "force_fast":
            mode = "fast"
            continue

        if mode == "explore":
            mm.speed = EXPLORE_SPEEDS[min(explore_count, len(EXPLORE_SPEEDS) - 1)]
            try:
                run_explore_leg(mm, memory, mm.center_cells)
                # only continue to return-leg if it wasn't aborted -
                # but since we're counting aborts as done anyway, check is_solved
                if is_solved(memory, mm.x, mm.y):
                    time.sleep(2)
                    run_explore_leg(mm, memory, [mm.start_cell])
            except RuntimeError:
                mm.led_red_set(True)
                continue

        else: # fast
            mm.speed = FAST_SPEED_FIRST if fast_count == 0 else FAST_SPEED_DEFAULT

            try:
                fast_run(mm, memory)
            except RuntimeError:
                mm.led_red_set(True)
                continue
            fast_count += 1

