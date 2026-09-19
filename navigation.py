from memory import Memory, N, E, S, W
from flood_fill import update_flood, get_next_move, is_solved, get_full_path
from movement import move_forward_one_cell, turn_left, turn_right, move_x_cells, turn_180
from micromouse import Micromouse






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
    next_dir = get_next_move(memory, mm.x, mm,y)

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



# Main Control Loop
def run(mm, memory):
    # Setup
    memory.mark_visted(mm.x, mm.y)

    # button interupt logic

    # reset button logic

    # timer logic

    # Explore Runs

    # Fast run



    return
