from memory import N, E, S, W


# Flood fil algorithm
def update_flood(memory, goal_cells):
    # Reset flood info to "unknown" distance
    for x in range(memory.width):
        for y in range(memory.height):
            memory.set_flood(x, y, 255)

    queue = []
    for (gx, gy) in goal_cells:
        memory.set_flood(gx, gy, 0)
        queue.append((gx, gy))

    while queue:
        x, y = queue.pop(0)
        current_value = memory.get_flood(x, y)

        for direction in (N, E, S, W):
            if memory.has_wall(x, y, direction):
                continue
            nx, ny = step(x, y, direction)

            if not (0 <= nx < memory.width and 0 <= ny < memory.height):
                continue

            if memory.get_flood(nx, ny) != 255:
                continue

            memory.set_flood(nx, ny, current_value + 1)
            queue.append((nx, ny))


def get_next_move(memory, x, y):
    best_direction = None
    best_value = 256

    for direction in (N, E, S, W):
        if memory.has_wall(x, y, direction):
            continue

        nx, ny = step(x, y, direction)

        if not (0 <= nx < memory.width and 0 <= ny < memory.height):
            continue

        value = memory.get_flood(nx, ny)
        if value < best_value:
            best_value = value
            best_direction = direction

    ###################################################### Add preference when tied, if wanted

    return best_direction

def is_solved(memory, x, y):
    return memory.get_flood(x, y) == 0

def get_full_path(memory, start, goal_cells):
    x, y = start
    path = []

    while (x,y) not in goal_cells:
        direction = get_next_move(memory,x, y)

        if direction is None:
            raise RuntimeError(f"get_full_path stuck at ({x}, {y}), goal unreachable")

        path.append(direction)
        x, y = step(x, y, direction)

    return path

def step(x, y, direction):
    if direction == N: return (x, y + 1)
    if direction == S: return (x, y - 1)
    if direction == E: return (x + 1, y)
    if direction == W: return (x - 1, y)
    raise ValueError(f"Unexpected direction: {direction}")



