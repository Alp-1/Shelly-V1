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
import numpy as np



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


pid_forward_flop= PID(0.2,0,0, 0)
pid_forward_flop.sample_time = 0.00000001
pid_forward_flop.output_limits = (-300,300)

def map_to_value(v1):
    start1, end1 = -300,300
    dead_zone_start, dead_zone_end = 1500,1630
    start2_low, end2_low =510, dead_zone_start
    start2_high, end2_high = dead_zone_end, 1490
    #mapped1 = start2 + (end2-start2)*(v1-start1)/(end1-start1)
    #mapped2 = start2 + (end2-start2)*(v2-start2)/(end-start1)
    
    if v1 < 0:
        base_mapped = start2_low + (end2_low - start2_low)* ((v1-start1) / (0 - start1))
    else:
        base_mapped = start2_high + (end2_high - start2_high)* ((v1-0) / (end1 - 0))
        
    # t= time.time()%10
    # cosine_adjustment = amplitude*np.cos(2*np.pi*0.05*t) # 0.5 freq
    # pwm_value = center_pwm + cosine_adjustment
    # pwm_value = max(min(pwm_value,base_mapped), 600, min(pwm_value,base_mapped,2500))
    return int(base_mapped)    

def stop_motion(left_motor_pin,right_motor_pin):
    self.pi.set_servo_pulsewidth(left_motor_pin, 1000)
    self.pi.set_servo_pulsewidth(right_motor_pin, 1000)

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
    start = False
    mode = 1
    speed_mode = 1
    pi = None
    mission_array = []
    start_mission = False
    
    def __init__(self):
        # Initialization code
        global global_angular_velocity
        self.pi = pigpio.pi()
        if not self.pi.connected:
            print("no connection")
            exit()

        self.pi.set_mode(self.left_motor_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.right_motor_pin, pigpio.OUTPUT)

        
        # Initialization
        movement_functions_ground.initialise_neutral_point(self.left_motor_pin,self.right_motor_pin)
        time.sleep(1)

        # Main loop
        try:
            #get_angular_velocity()
            t3 = Thread(target=get_heading,args=(self.start,))
            t3.setDaemon(True)
            t3.start()
            t4 = Thread(target=self.controlLoop)
            t4.setDaemon(True)
            t4.start()
            t5 = Thread(target=get_encoder_data)
            t5.setDaemon(True)
            t5.start()
        except KeyboardInterrupt:
            pi.set_servo_pulsewidth(self.left_motor_pin, 1000)
            pi.set_servo_pulsewidth(self.right_motor_pin, 1000)
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
        #angsetpoint1 = 20
        #angsetpoint2 = 1
        i = 0
        
        ##water-up motion
        angles_up_up = np.linspace(120,220, num = 5) 
        angles_down_up = np.linspace(220,120, num = 5)
        angles_up = np.concatenate((angles_up_up,angles_down_up))
        
        ##water-down motion
        angles_up_down = np.linspace(300,60, num = 3) 
        angles_down_down = np.linspace(60,300, num = 3)
        angles_down = np.concatenate((angles_up_down,angles_down_down))
        
        ##water-front motion
        angles_up_front = np.linspace(30,150, num = 5) 
        angles_down_front = np.linspace(150,30, num = 5)
        angles_forward = np.concatenate((angles_up_front,angles_down_front))
        
        ##water-back motion
        angles_up_back = np.linspace(330,210, num = 3)
        angles_down_back = np.linspace(210,330, num = 3)
        angles_backward = np.concatenate((angles_up_front,angles_down_front))
        
        ##water-right motion
        angles_up_right_rm = np.linspace(30,150, num = 3)
        angles_down_right_rm = np.linspace(150,30, num = 3)
        angles_right_rm = np.concatenate((angles_up_front,angles_down_front))
        
        angles_up_right_lm = np.linspace(330,210, num = 3)
        angles_down_right_lm = np.linspace(210,330, num = 3)
        angles_right_lm = np.concatenate((angles_up_front,angles_down_front))
            
        ##water-left motion
        angles_up_left_rm = np.linspace(330,210, num = 3)
        angles_down_left_rm = np.linspace(210,330, num = 3)
        angles_left_rm = np.concatenate((angles_up_front,angles_down_front))
        
        angles_up_left_lm = np.linspace(30,150, num = 3)
        angles_down_left_lm = np.linspace(150,30, num = 3)
        angles_left_lm = np.concatenate((angles_up_front,angles_down_front))
        
        #time definitions
        
        #if flag_forward: 
        #    anglesR = angles_forward
        #    anglesL = angles_forward 
        #    total_time = total_time_forward 
        #elif flag_backward:
        #    anglesR = angles_backward
        #    anglesL = angles_forward 
        #    total_time = total_time_backward
        #elif flag_left:
        #    anglesR = angles_left_rm
        #    anglesL = angles_left_lm
        #    total_time = total_time_left
        #elif flag_right:
        #    anglesR = angles_right_rm
        #    anglesL = angles_right_lm
        #    total_time = total_time_right 
        #elif flag_up:
        #    anglesR = angles_up
        #    anglesL = angles_up
        #    total_time = total_time_up 
        #elif flag_down:
        #    anglesR = angles_down
        #    anglesL = angles_down
        #    total_time = total_time_down 
        
        


        
        while True:
            current_time = time.time()
            elapsed_time = current_time-start_time
            
            
            time_interval = total_time/len (anglesR)
            
            start_time = time.time()
            
            current_setpoint_indexR = 0
            current_setpoint_indexL = 0
            angsetpointR= anglesR[current_setpoint_indexR]
            angsetpointL= anglesL[current_setpoint_indexL]
            
            if current_time - start_time >= time_interval:
                
                current_setpoint_indexR = (current_setpoint_indexR + 1)%len(anglesR)
                current_setpoint_indexL = (current_setpoint_indexL + 1)%len(anglesL)
                angsetpointR = anglesR[current_setpoint_indexR]
                angsetpointL = anglesL[current_setpoint_indexL]
                setpoint_change_time = current_time
                    

                       

            movement_functions.forward(left_motor_pin,right_motor_pin,angle1,angle2,angsetpointR,angsetpointL)
                    #i += 1
            if elapsed_time >= total_time:
                start_time=time.time()
                setpoint_change_time = start_time
                current_setpoint_indexR = 0
                current_setpoint_indexL = 0
                
                ## Singular Position Test Logic
                #print(f"Current setpoint: {angsetpoint1} degrees at index {current_setpoint_index}")
                    #if i == 3000:
                    #	angsetpoint1 = 78
                  
                    #elif i>3000:
                    #	angsetpoint1 = 127
                    #	print("second") 
        angsetpoint1 = 1
        while True:
            if self.mode == 1:
                #print(self.flag_forward,self.flag_stop,self.flag_back,self.flag_left,self.flag_right)
                if self.flag_forward == True and self.flag_stop == False and self.flag_back == False and self.flag_right == False and self.flag_left==False:
                    movement_functions_ground.forward_hard(self.left_motor_pin,self.right_motor_pin,self.speed_mode)
                elif self.flag_back == True and self.flag_stop == False and self.flag_forward == False and self.flag_right == False and self.flag_left==False:
                    #movement_functions_ground.set_heading(global_heading) 
                    #movement_functions_ground.backward(self.left_motor_pin,self.right_motor_pin,self.speed_mode,rpm1,rpm2)
                    movement_functions_ground.backward_hard(self.left_motor_pin,self.right_motor_pin,self.speed_mode)
                elif self.flag_left == True and self.flag_stop == False and self.flag_forward == False and self.flag_right== False and self.flag_back==False:
                    #movement_functions_ground.set_heading(global_heading) 
                    #movement_functions_ground.left(self.left_motor_pin,self.right_motor_pin,self.speed_mode,rpm1,rpm2)
                    movement_functions_ground.left_hard(self.left_motor_pin,self.right_motor_pin,self.speed_mode)
                elif self.flag_right == True and self.flag_stop == False and self.flag_forward == False and self.flag_back== False and self.flag_left==False:
                    #movement_functions_ground.set_heading(global_heading) 
                    #movement_functions_ground.right(self.left_motor_pin,self.right_motor_pin,self.speed_mode,rpm1,rpm2)
                    movement_functions_ground.right_hard(self.left_motor_pin,self.right_motor_pin,self.speed_mode)
                else:
                    movement_functions_ground.stop_motion(self.left_motor_pin,self.right_motor_pin)
            elif self.mode == 2 and self.start_mission:
                print(self.mission_array)
                for arr in self.mission_array:
                    total_time = arr[1]
                    command = arr[0]
                    elapsed_time = 0
                    begin_time = time.time()
                    set_point_change_time = time.time()
                    current_setpoint_indexR = 0
                    current_setpoint_indexL = 0
                    while elapsed_time <= total_time:
                        if command == "Forward":
                            anglesR = angles_forward
                            anglesL = angles_forward
                            
                        elif command == "Backward":
                            anglesR = angles_backward
                            anglesL = angles_backward
                            
                        elif command == "Up":
                            anglesR = angles_up
                            anglesL = angles_up
                            
                        elif command == "Down":
                            anglesR = angles_down
                            anglesL = angles_down
                            
                        elif command == "Right":
                            anglesR = angles_right_rm
                            anglesL = angles_right_rm
                            
                        elif command == "Left":
                            anglesR = angles_left_rm
                            anglesL = angles_left_rm
                        time_interval = total_time/len (anglesR)
                        current_time = time.time()
                        elapsed_time = current_time-begin_time
                        
                            
                        if current_time - setpoint_change_time >= time_interval:
                            current_setpoint_indexR = (current_setpoint_indexR + 1)%len(anglesR)
                            current_setpoint_indexL = (current_setpoint_indexL + 1)%len(anglesL)
                            angsetpointR = anglesR[current_setpoint_indexR]
                            angsetpointL = anglesL[current_setpoint_indexL]
                            setpoint_change_time = current_time
                            
                        movement_functions.forward(left_motor_pin,right_motor_pin,angle1,angle2,angsetpointR,angsetpointL)


