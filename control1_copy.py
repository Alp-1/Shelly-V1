import pigpio
import threading
import smbus
import time
import math
from simple_pid import PID
import movement_functions
import movement_functions_ground
import keyboard

pi = pigpio.pi()

global_angular_velocity = 0
bus = smbus.SMBus(1)

# Address for Encoder
AS5600_ADDRESS = 0x36
RAW_ANGLE_HIGH = 0x0C
RAW_ANGLE_LOW = 0x0D
STATUS_REGISTER = 0x0B

# Globals for encoder
previous_angle = None
previous_time = None
global_sign = None

    
def forward(left_motor_pin,right_motor_pin,speed_mode):
    
    if speed_mode == 1: #Slow

     pi.set_servo_pulsewidth(left_motor_pin, 1850)
     pi.set_servo_pulsewidth(right_motor_pin, 1850)
     print("Going forward")
    
    else:
        print("invalid speed mode")
        
        
def stop_motion(left_motor_pin, right_motor_pin):
    pi.set_servo_pulsewidth(left_motor_pin, 1550) #(+- 50 deadzone max(600, 2500) (Neutral set at 1550)
    pi.set_servo_pulsewidth(right_motor_pin, 1550)

def read_raw_angle():
    global bus, AS5600_ADDRESS, RAW_ANGLE_HIGH, RAW_ANGLE_LOW
    highbyte = bus.read_byte_data(AS5600_ADDRESS, RAW_ANGLE_HIGH)
    lowbyte = bus.read_byte_data(AS5600_ADDRESS, RAW_ANGLE_LOW)
    raw_angle = (highbyte << 8) | lowbyte
    return raw_angle * 360.0 / 4096.0


def calculate_angular_velocity():
    global previous_angle, previous_time,global_sign
    
    current_time = time.time()
    raw_angle = read_raw_angle()

    current_angle = raw_angle
    
    if previous_angle is None or previous_time is None:
        previous_angle = current_angle
        previous_time = current_time
        return 0.0  # Cannot calculate velocity on first measurement

    # Time delta in seconds
    time_delta = current_time - previous_time
    if time_delta == 0:
        return 0.0  # Prevent division by zero

    # Calculate angle difference and adjust for wrapping
    angle_delta = current_angle - previous_angle
    if angle_delta<0 and global_sign == True:
        angle_delta+=360
    elif angle_delta>0 and global_sign == False:
        angle_delta-=360
    
    
    #print("delta ",angle_delta)
    #print("current angle ", current_angle)
    #print ("previous angle ",previous_angle)
    
    # Angular velocity in degrees per second
    angular_velocity = angle_delta / time_delta
    
    
    #print ("velocity deg/s ",angular_velocity)
    
    #if angle_delta <0 or angular_velocity>1000:
     #   exit()
    
    # Update previous values
    previous_angle = current_angle
    previous_time = current_time
    global_sign = angle_delta>0

    return -angular_velocity
    
def get_angular_velocity():
    global global_angular_velocity
    while True:
        l=0
        sum1=0
        avg=0
        for i in range(10):
            transfer = calculate_angular_velocity()
            if transfer > 10000 or transfer >-10000:
                continue
            else:
                sum1 +=transfer
                l+=1
                avg=sum1/l
        global_angular_velocity = avg
                
        time.sleep(0.01)

class Controller:
    #UI Flags
    flag_forward = False
    flag_stop = True
    flag_left = False
    flag_right = False
    flag_back = False
    mode= 2 #1 ground #2 water

    # Additional variables for angular velocity calculation

    left_motor_pin = 12
    right_motor_pin = 19
    
    speed_mode = 1
    
    def __init__(self):
        # Initialization code
        global global_angular_velocity
        pi = pigpio.pi()
        if not pi.connected:
            print("no connection")
            exit()

        pi.set_mode(self.left_motor_pin, pigpio.OUTPUT)
        pi.set_mode(self.right_motor_pin, pigpio.OUTPUT)

        
        # Initialization
        movement_functions_ground.initialise_neutral_point(self.left_motor_pin,self.right_motor_pin)
        time.sleep(5)


        # Main loop
        try:
            #get_angular_velocity()
            #t1 = threading.Thread(target=get_angular_velocity, name="t1", args=())
            #t1.start()
            t2 = threading.Thread(target=self.controlLoop, name="t2", args=())
            t2.start()
            
        except KeyboardInterrupt:
            pi.set_servo_pulsewidth(self.left_motor_pin, 1550)
            pi.set_servo_pulsewidth(self.right_motor_pin, 1550)
            pi.stop()
            print("Program stopped by the user.")
            
        finally:
            pi.set_servo_pulsewidth(self.left_motor_pin, 1550)
            pi.set_servo_pulsewidth(self.right_motor_pin, 1550)
            pi.stop()
            print("Program stopped by the user.")
            
    def controlLoop(self):
        while True:
            if self.mode == 1:
                if self.flag_forward == True and self.flag_stop == False and self.flag_back == False and self.flag_right== False and self.flag_left==False: 
                    forward(self.left_motor_pin,self.right_motor_pin,self.speed_mode)
                    
                    #movement_functions_ground.forward(self.left_motor_pin,self.right_motor_pin,self.speed_mode)
                #elif self.flag_back == True and self.flag_stop == False and self.flag_forward == False and self.flag_right== False and self.flag_left==False:
                #     movement_functions_ground.backward(self.left_motor_pin,self.right_motor_pin,self.speed_mode)
                #elif self.flag_left == True and self.flag_stop == False and self.flag_forward == False and self.flag_right== False and self.flag_back==False:
                #     movement_functions_ground.left(self.left_motor_pin,self.right_motor_pin,self.speed_mode)
                #elif self.flag_right == True and self.flag_stop == False and self.flag_forward == False and self.flag_back== False and self.flag_left==False:
                #     movement_functions_ground.right(self.left_motor_pin,self.right_motor_pin,self.speed_mode)
                else:
                    stop_motion(self.left_motor_pin,self.right_motor_pin)
            #elif self.mode == 2:
            #    movement_functions.sequence_driver(self.left_motor_pin,self.right_motor_pin,self.encoder_position,self.action_list,self.spacing,self.speed_mode)
            #    self.action_list=[] # clean action list 
             

