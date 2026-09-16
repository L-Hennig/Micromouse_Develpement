"""
Filename: tof_test_v_1.py
Description: Standalone bench test for the VL53L4CD ToF sensor on the Pico.
Uses hardware I2C0 on GP4 (SDA) / GP5 (SCL).
Uses the manual measurement loop (data_ready / clear_interrupt) rather
than the get_distance() convenience wrapper in vl53l4cd.py, since that
wrapper silently retries recursively on any OSError.

Requires vl53l4cd.py and i2c_device.py to already be on the Pico,
in the same directory as this file.
"""
from machine import I2C, Pin
from vl53l4cd import VL53L4CD
import time

# --- I2C setup ---
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)

# Quick sanity check: confirm the sensor is visible on the bus before
# trying to talk to it via the driver.
devices = i2c.scan()
print("I2C devices found:", [hex(d) for d in devices])

if not devices:
    print("No I2C devices found. Check wiring, power, and pull-ups"
          " before continuing.")

# --- Sensor setup ---
vl53 = VL53L4CD(i2c)

# OPTIONAL: can set non-default values
vl53.inter_measurement = 0   # continuous mode
vl53.timing_budget = 20      # ms spent per measurement

print("VL53L4CD Simple Test.")
print("--------------------")
model_id, module_type = vl53.model_info
print("Model ID: 0x{:0X}".format(model_id))
print("Module Type: 0x{:0X}".format(module_type))
print("Timing Budget: {}".format(vl53.timing_budget))
print("Inter-Measurement: {}".format(vl53.inter_measurement))
print("--------------------")

vl53.start_ranging()

# A KeyboardInterrupt here (stop button in Thonny) is a deliberate,
# manual stop, not a program error.
try:
    while True:
        while not vl53.data_ready:
            time.sleep_ms(5)
        vl53.clear_interrupt()
        print("Distance: {} cm".format(vl53.distance))
except KeyboardInterrupt:
    vl53.stop_ranging()
    print("Stopped by user.")
