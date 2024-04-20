import smbus
import time

# Constants
AS5600_ADDRESS = 0x36
RAW_ANGLE_HIGH = 0x0C
RAW_ANGLE_LOW = 0x0D
STATUS_REGISTER = 0x0B

# Variables
start_angle = 0.0
number_of_turns = 0
previous_quadrant_number = 0
previous_total_angle = 0.0

# Create an SMBus instance for I2C communication
bus = smbus.SMBus(1)

def read_raw_angle():
    highbyte = bus.read_byte_data(AS5600_ADDRESS, RAW_ANGLE_HIGH)
    lowbyte = bus.read_byte_data(AS5600_ADDRESS, RAW_ANGLE_LOW)
    raw_angle = (highbyte << 8) | lowbyte
    return raw_angle * 360.0 / 4096.0

def check_magnet_presence():
    while True:
        magnet_status = bus.read_byte_data(AS5600_ADDRESS, STATUS_REGISTER)
        if magnet_status & 0b00100000 == 0b00100000:
            break  # Magnet is detected
        time.sleep(0.1)

def check_quadrant(corrected_angle):
    global number_of_turns, previous_quadrant_number

    # Determine the current quadrant
    quadrant_number = 0
    if 0 <= corrected_angle <= 90:
        quadrant_number = 1
    elif 90 < corrected_angle <= 180:
        quadrant_number = 2
    elif 180 < corrected_angle <= 270:
        quadrant_number = 3
    elif 270 < corrected_angle < 360:
        quadrant_number = 4

    # Detect full rotation
    if quadrant_number == 1 and previous_quadrant_number == 4:
        number_of_turns += 1
    elif quadrant_number == 4 and previous_quadrant_number == 1:
        number_of_turns -= 1

    previous_quadrant_number = quadrant_number

    return quadrant_number

# Initialization
check_magnet_presence()
start_angle = read_raw_angle()

# Main loop
try:
    while True:
        raw_angle = read_raw_angle()
        corrected_angle = raw_angle - start_angle
        corrected_angle = corrected_angle + 360 if corrected_angle < 0 else corrected_angle

        quadrant_number = check_quadrant(corrected_angle)
        total_angle = (number_of_turns * 360) + corrected_angle

        # Print the current angle to the console
        print("Total Angle: %.2f degrees" % total_angle)
        print("Raw Angle: %.2f degrees" % raw_angle)

        # Insert a short delay to throttle the output and CPU usage
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program stopped by the user.")