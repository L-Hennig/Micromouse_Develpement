"""
Filename: tof_drive_test_v_2.py
Description: Bench test that drives the mouse forward and stops when the
VL53L4CD ToF sensor detects an object within STOP_DISTANCE_MM. Same as
tof_drive_test_v_1.py, but applies the tof_calibration.calibrate()
correction to the raw sensor reading before comparing against the
threshold, since the raw reading over-reports at short range.

Requires vl53l4cd.py, i2c_device.py, and tof_calibration.py to already
be on the Pico.
"""
from machine import I2C, Pin
from vl53l4cd import VL53L4CD
from micromouse import Micromouse
from tof_calibration import calibrate

STOP_DISTANCE_MM = 100

mm = Micromouse()

# --- ToF sensor setup (GP4/GP5, matches earlier wiring) ---
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
vl53 = VL53L4CD(i2c)
vl53.inter_measurement = 0   # continuous mode
vl53.timing_budget = 20      # ms per measurement
vl53.start_ranging()

print("Driving until an object is detected within {} mm...".format(STOP_DISTANCE_MM))

# A KeyboardInterrupt here (stop button in Thonny) is a deliberate,
# manual stop, not a program error.
try:
    while True:
        while not vl53.data_ready:
            pass
        vl53.clear_interrupt()
        raw_mm = vl53.distance * 10  # driver reports cm, convert to mm
        corrected_mm = calibrate(raw_mm)

        if corrected_mm < STOP_DISTANCE_MM:
            mm.drive_stop()
            print("Object detected at {:.1f} mm (raw {:.1f} mm) - stopping"
                  .format(corrected_mm, raw_mm))
        else:
            mm.drive_forward()
except KeyboardInterrupt:
    mm.drive_stop()
    vl53.stop_ranging()
    print("Stopped by user.")
