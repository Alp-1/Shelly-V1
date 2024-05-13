import pigpio
from threading import *
import smbus
import time
import math
from simple_pid import PID
import movement_functions
import movement_functions_ground
import keyboard
import serial
from queue import Queue
from multiprocessing import Process, Value

#serial initialisation
ser = serial.Serial(
	port='/dev/ttyACM1',
	baudrate=115200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)
ser1 = serial.Serial('/dev/ttyACM0', 115200,timeout=1)

#globals
angvel1=0
rpm1=0
angle1=0
angvel2=0
rpm2=0
angle2=0
start = False
global_heading = 0

def is_float(string):
     if string.replace(".","").isnumeric():
         return True
     else:
         return False

def get_heading(start):
    global global_heading
    a=0
    while True:
        if ser.in_waiting>0:
             data=ser.readline().decode('utf-8').strip()
             data=data.strip()
             try:
                  if is_float(data):
                     if start:
                         set_target(float(data))
                         start = False
                     global_heading = float(data)
             except:
                  print("Oops")

def get_encoder_data():
    global angvel1
    global rpm1
    global angle1
    global angvel2
    global rpm2
    global angle2
    try:
        while True:
            line = ser1.readline().decode().strip()  # Read a line from the Pico
            if line:
                parts = line.split()
                if len(parts) == 4:
                    encoder_id = int(parts[0])  # Encoder identifier
                    angular_velocity = float(parts[1])
                    rpm = float(parts[2])
                    raw_angle = float(parts[3])
                    
                    # Assign values to variables based on encoder ID
                    if encoder_id == 1:
                        angvel1 = angular_velocity
                        rpm1 = rpm
                        angle1 = raw_angle
                        print(angle1)
                    elif encoder_id == 2:
                        angvel2 = angular_velocity
                        rpm2 = rpm
                        angle2 = raw_angle

    finally:
        ser.close()  # Always close the serial connection when done

class Controller:
    #UI Flags
    processes = []

    # Additional variables for angular velocity calculation

    left_motor_pin = 19
    right_motor_pin = 12
    flag_forward = False
    flag_back = False
    flag_left = False
    flag_right = False
    flag_stop = True
    mode = 1
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
        time.sleep(1)

        # Main loop
        try:
            #get_angular_velocity()
            #t3 = Thread(target=get_encoder_data)
            #t3.setDaemon(True)
            #t3.start()
            t4 = Thread(target=self.controlLoop)
            t4.setDaemon(True)
            t4.start()
            #t5 = Thread(target=get_heading)
            #t5.setDaemon(True)
            #t5.start()
        except KeyboardInterrupt:
            pi.set_servo_pulsewidth(self.left_motor_pin, 1550)
            pi.set_servo_pulsewidth(self.right_motor_pin, 1550)
            pi.stop()
            print("Program stopped by the user.")
            
    def controlLoop(self):
        global global_heading
        global angvel1
        global rpm1
        global angle1
        global angvel2
        global rpm2
        global angle2
        i=0
        angsetpoint1 = 60
        angsetpoint2 = 60
        while True:
            if self.mode == 1:
                #print(self.flag_forward,self.flag_stop,self.flag_back,self.flag_left,self.flag_right)
                if self.flag_forward == True and self.flag_stop == False and self.flag_back == False and self.flag_right == False and self.flag_left==False:
                    #movement_functions_ground.set_heading(global_heading) 
                    #movement_functions_ground.forward(self.left_motor_pin,self.right_motor_pin,self.speed_mode,rpm1,rpm2)
                    #if i == 10:
                     #   angsetpoint1 = 60
                      #  angsetpoint2 = 60
                       # i =0 
                    movement_functions.forward(self.left_motor_pin,self.right_motor_pin,angle1,angle2,angsetpoint1,angsetpoint2)
                    #pid_update(currangle, setpoint)
                    #i+=1 
                elif self.flag_back == True and self.flag_stop == False and self.flag_forward == False and self.flag_right == False and self.flag_left==False:
                    movement_functions_ground.set_heading(global_heading) 
                    #movement_functions_ground.backward(self.left_motor_pin,self.right_motor_pin,self.speed_mode,rpm1,rpm2)
                    movement_functions_ground.backward_hard(self.left_motor_pin,self.right_motor_pin,self.speed_mode)
                elif self.flag_left == True and self.flag_stop == False and self.flag_forward == False and self.flag_right== False and self.flag_back==False:
                    movement_functions_ground.set_heading(global_heading) 
                    #movement_functions_ground.left(self.left_motor_pin,self.right_motor_pin,self.speed_mode,rpm1,rpm2)
                    movement_functions_ground.left_hard(self.left_motor_pin,self.right_motor_pin,self.speed_mode)
                elif self.flag_right == True and self.flag_stop == False and self.flag_forward == False and self.flag_back== False and self.flag_left==False:
                    movement_functions_ground.set_heading(global_heading) 
                    #movement_functions_ground.right(self.left_motor_pin,self.right_motor_pin,self.speed_mode,rpm1,rpm2)
                    movement_functions_ground.right_hard(self.left_motor_pin,self.right_motor_pin,self.speed_mode)
                else:
                    movement_functions_ground.stop_motion(self.left_motor_pin,self.right_motor_pin)
            #elif self.mode == 2:
            #    movement_functions.sequence_driver(self.left_motor_pin,self.right_motor_pin,self.encoder_position,self.action_list,self.spacing,self.speed_mode)
            #    self.action_list=[] # clean action list 
             

