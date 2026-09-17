"""
Filename: tof_calibration.py
Description: Calibration correction for the VL53L4CD, built from bench
accuracy-test data (actual distance vs. sensor-reported distance, in mm).
The raw sensor reading is not linear - it over-reports at short range
and under-reports past ~300mm - so this module linearly interpolates
between the measured calibration points to recover a corrected distance.

Table format: (actual_mm, measured_mm), sorted by actual distance.
"""

# (actual_mm, measured_mm)
CALIBRATION_TABLE_1 = [
    (10, 15.9),
    (15, 20.7),
    (20, 26.6),
    (25, 32.86),
    (30, 37.26),
    (35, 43.05),
    (40, 49.77),
    (45, 54.63),
    (50, 60.94),
    (55, 65.06),
    (60, 71.08),
    (65, 75.81),
    (70, 80.86),
    (75, 86.63),
    (80, 92.19),
    (85, 97.89),
    (90, 102.85),
    (95, 108.44),
    (100, 113.31),
    (105, 118.31),
    (110, 124.42),
    (115, 127.62),
    (120, 133.29),
    (125, 138.29),
    (130, 143.96),
    (135, 149.66),
    (140, 154.33),
    (145, 158.03),
    (150, 164.49),
    (155, 170.41),
    (160, 175.99),
    (165, 179.54),
    (170, 186.03),
    (175, 188.99),
    (180, 192.29),
    (185, 198.14),
    (190, 203.63),
    (195, 209.04),
    (200, 213.74),
    (205, 217.44),
    (210, 221.64),
    (215, 227.08),
    (220, 233),
    (225, 237.98),
    (230, 243.27),
    (235, 247.62),
    (240, 251.49),
    (245, 256.84),
    (250, 261.06),
    (255, 266.24),
    (260, 270.29),
    (265, 275.76),
    (270, 280),
    (275, 284.05),
    (280, 289.56),
    (285, 294.88),
    (290, 298.77),
    (295, 303.78),
    (300, 309.52),
    (350, 354.68),
    (400, 402.6),
    (450, 446.96),
    (550, 534.8),
    (600, 577.57),
]

CALIBRATION_TABLE_2 = [
    (9.50, 10),
    (16.09, 15),
    (23.34, 20),
    (30.77, 25),
    (36.87, 30),
    (42.39, 35),
    (48.60, 40),
    (54.43, 45),
    (58.76, 50),
    (64.83, 55),
    (69.98, 60),
    (74.74, 65),
    (79.81, 70),
    (84.78, 75),
    (90.58, 80),
    (94.86, 85),
    (99.84, 90),
    (105.48, 95),
    (110.78, 100),
    (115.50, 105),
    (120.90, 110),
    (125.66, 115),
    (130.84, 120),
    (135.49, 125),
    (139.44, 130),
    (143.04, 135),
    (147.94, 140),
    (153.66, 145),
    (159.34, 150),
    (164.14, 155),
    (169.56, 160),
    (174.56, 165),
    (179.17, 170),
    (184.11, 175),
    (189.63, 180),
    (194.76, 185),
    (199.48, 190),
    (204.22, 195),
    (210.02, 200),
    (214.20, 205),
    (218.55, 210),
    (223.57, 215),
    (228.44, 220),
    (233.63, 225),
    (238.13, 230),
    (242.68, 235),
    (247.92, 240),
    (252.38, 245),
    (256.45, 250),
    (260.92, 255),
    (265.87, 260),
    (270.33, 265),
    (274.76, 270),
    (279.32, 275),
    (283.94, 280),
    (287.98, 285),
    (292.17, 290),
    (296.89, 295),
    (301.62, 300),
    (345.60, 350),
    (386.48, 400),
    (428.16, 450),
    (463.95, 500),
    (502.57, 550),
    (533.89, 600),
]


CALIBRATION_TABLE_3 = [
    (12.59, 10),
    (19.30, 15),
    (26.86, 20),
    (32.66, 25),
    (37.98, 30),
    (42.82, 35),
    (48.38, 40),
    (53.94, 45),
    (59.77, 50),
    (64.86, 55),
    (69.81, 60),
    (75.14, 65),
    (80.60, 70),
    (85.00, 75),
    (89.74, 80),
    (94.74, 85),
    (100.21, 90),
    (105.32, 95),
    (110.49, 100),
    (115.46, 105),
    (120.82, 110),
    (125.41, 115),
    (129.92, 120),
    (135.64, 125),
    (140.43, 130),
    (146.38, 135),
    (150.51, 140),
    (153.53, 145),
    (158.49, 150),
    (163.20, 155),
    (168.16, 160),
    (172.55, 165),
    (176.67, 170),
    (181.49, 175),
    (186.39, 180),
    (190.97, 185),
    (196.25, 190),
    (200.84, 195),
    (205.32, 200),
    (209.80, 205),
    (214.57, 210),
    (219.26, 215),
    (224.25, 220),
    (228.19, 225),
    (232.35, 230),
    (236.77, 235),
    (241.82, 240),
    (246.48, 245),
    (251.34, 250),
    (254.58, 255),
    (258.94, 260),
    (262.33, 265),
    (265.84, 270),
    (266.20, 275),
    (273.96, 280),
    (278.41, 285),
]

CALIBRATION_TABLES = {
    1: CALIBRATION_TABLE_1,
    2: CALIBRATION_TABLE_2,
    3: CALIBRATION_TABLE_3
}

def calibrate(measured_mm, sensor_num):
    """
    Converts a raw sensor-reported distance (mm) into a corrected
    real-world distance (mm) by linearly interpolating between the
    nearest calibration points.

    Parameters:
        measured_mm (float): The raw distance reported by the sensor.
        sensor_num (int): The sensor ID number

    Returns:
        float: The corrected, real-world distance estimate in mm.
    """
    table = CALIBRATION_TABLES[sensor_num]
    # Below the lowest calibration point: extrapolate using the first
    # segment's slope.
    if measured_mm <= table[0][1]:
        (a0, m0) = table[0]
        (a1, m1) = table[1]
        slope = (a1 - a0) / (m1 - m0)
        return a0 + slope * (measured_mm - m0)

    # Above the highest calibration point: extrapolate using the last
    # segment's slope.
    if measured_mm >= table[-1][1]:
        (a0, m0) = table[-2]
        (a1, m1) = table[-1]
        slope = (a1 - a0) / (m1 - m0)
        return a1 + slope * (measured_mm - m1)

    # Otherwise, find the bracketing pair and interpolate between them.
    for i in range(len(table) - 1):
        (a0, m0) = table[i]
        (a1, m1) = table[i + 1]
        if m0 <= measured_mm <= m1:
            fraction = (measured_mm - m0) / (m1 - m0)
            return a0 + fraction * (a1 - a0)

    # Should not be reached, but fall back to the raw value if it is.
    return measured_mm
