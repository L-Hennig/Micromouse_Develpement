import math

# Test encoder count with mouse again(giving variable results)!
ENCODER_COUNT_PER_WHEEL_REV = 718
WHEEL_SPACING = 93
ENCODER_COUNT_CELL = int(1.433 * ENCODER_COUNT_PER_WHEEL_REV) 


def move_forward_one_cell(mm):
    start_1 = mm.motor_1.encoder_read()
    start_2 = mm.motor_2.encoder_read()

    mm.motor_1.spin_forward(80)
    mm.motor_2.spin_forward(80)

    while True:
        count_1 = abs(mm.motor_1.encoder_read() - start_1)
        count_2 = abs(mm.motor_2.encoder_read() - start_2)

        if count_1 >= ENCODER_COUNT_CELL or count_2 >= ENCODER_COUNT_CELL:
            break

    mm.motor_1.spin_stop()
    mm.motor_2.spin_stop()



def turn_left(mm):
    start_1 = mm.motor_1.encoder_read()
    start_2 = mm.motor_2.encoder_read()
    
    # needs to turn quarter of circle w diameter of wheel spacing for 90deg
    turn_distance = math.pi * WHEEL_SPACING / 4
    
    # pi x diameter of wheel
    wheel_circumference = math.pi * 40

    # encoder count for a 90deg turn
    encoder_count_turn = turn_distance / wheel_circumference * ENCODER_COUNT_PER_WHEEL_REV

    mm.motor_2.spin_backward(80)
    mm.motor_1.spin_forward(80)

    while True:
        count_1 = abs(mm.motor_1.encoder_read() - start_1)
        count_2 = abs(mm.motor_2.encoder_read() - start_2)
        if count_1 >= encoder_count_turn and count_2 >= encoder_count_turn:
            break

    mm.drive_stop()


def turn_right(mm):
    start_1 = mm.motor_1.encoder_read()
    start_2 = mm.motor_2.encoder_read()

    turn_distance = math.pi * WHEEL_SPACING / 4
    wheel_circumference = math.pi * 40

    encoder_count_turn = turn_distance / wheel_circumference * ENCODER_COUNT_PER_WHEEL_REV

    mm.motor_1.spin_backward(80)
    mm.motor_2.spin_forward(80)

    while True:
        count_1 = abs(mm.motor_1.encoder_read() - start_1)
        count_2 = abs(mm.motor_2.encoder_read() - start_2)
        if count_1 >= encoder_count_turn and count_2 >= encoder_count_turn:
            break

    mm.drive_stop()


def move_x_cells(mm, x):
    for i in range(x):
        move_forward_one_cell(mm)


def turn_180(mm):
    turn_left(mm)
    turn_left(mm)
