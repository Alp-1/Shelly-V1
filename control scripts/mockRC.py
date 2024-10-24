import pigpio
import time

pi = pigpio.pi()

# Ensure the Pi connected
if not pi.connected:
    print("no connection")
    exit()
    

# GPIO Pins for PWM
left_motor_pin = 12  # Example pin for left motor
right_motor_pin = 19 # Example pin for right motor

# Set the pins to output mode
pi.set_mode(left_motor_pin, pigpio.OUTPUT)
pi.set_mode(right_motor_pin, pigpio.OUTPUT)

# Initialize PWM signal for RC compatibility (neutral point at 1.5 ms)(1560 and 1440 is the minimum speed) (2500 to 550 max)
neutral_pulsewidth = 1550
pi.set_servo_pulsewidth(left_motor_pin, neutral_pulsewidth)
pi.set_servo_pulsewidth(right_motor_pin, neutral_pulsewidth)

# Run for a bit
time.sleep(2)

#pulsewidth = 2000
#pi.set_servo_pulsewidth(left_motor_pin, pulsewidth)
#pi.set_servo_pulsewidth(right_motor_pin, pulsewidth)

#time.sleep(5)

# Stop the motors
pi.set_servo_pulsewidth(left_motor_pin, 1600)
pi.set_servo_pulsewidth(right_motor_pin, 1600)

# Cleanup
pi.stop()
