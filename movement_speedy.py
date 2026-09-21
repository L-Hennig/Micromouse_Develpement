import math

ENCODER_COUNT_PER_WHEEL_REV = 718
WHEEL_SPACING = 93

# Function to move forward x squares 
## already in movement.


## maybe later: Function to turn x degrees

##turning left x degrees
def turn_left(mm, angle):
    start_1 = mm.motor_1.encoder_read()
    start_2 = mm.motor_2.encoder_read()

    # finding sector of circle made from wheel spacing
    turn_distance = math.pi * WHEEL_SPACING * angle / 360
    wheel_circumference = math.pi * 40

    encoder_count_turn = turn_distance / wheel_circumference * ENCODER_COUNT_PER_WHEEL_REV

    mm.motor_2.spin_backward(80)
    mm.motor_1.spin_forward(80)

    while True:
        count_1 = abs(mm.motor_1.encoder_read() - start_1)
        count_2 = abs(mm.motor_2.encoder_read() - start_2)

        if count_1 >= encoder_count_turn and count_2 >= encoder_count_turn:
            break

    mm.drive_stop()


# same as turn_left but opposite spin
def turn_right(mm, angle):
    start_1 = mm.motor_1.encoder_read()
    start_2 = mm.motor_2.encoder_read()

    turn_distance = math.pi * WHEEL_SPACING * angle / 360
    wheel_circumference = math.pi * 40

    encoder_count_turn = turn_distance / wheel_circumference * ENCODER_COUNT_PER_WHEEL_REV
    
    mm.motor_2.spin_forward(80)
    mm.motor_1.spin_backward(80)

    while True:
        count_1 = abs(mm.motor_1.encoder_read() - start_1)
        count_2 = abs(mm.motor_2.encoder_read() - start_2)

        if count_1 >= encoder_count_turn and count_2 >= encoder_count_turn:
            break

    mm.drive_stop()
