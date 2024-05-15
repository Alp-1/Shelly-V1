import pigpio
import threading
import smbus
import time
import math
from simple_pid import PID
import movement_functions
import movement_functions_ground
import keyboard
import serial
from multiprocessing import Process
import numpy as np
c1 = threading.Condition()

pid_forward_flop= PID(0.2,0,0, 0)
pid_forward_flop.sample_time = 0.00000001
pid_forward_flop.output_limits = (-300,300)

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

def get_heading():
    global global_heading
    global start
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
                     print(data)
             except:
                  print("Oops")

def get_encoder_data():
    global angvel1,rpm1,angle1,angvel2,rpm2,angle2
    try:
        while True:

            line = ser1.readline().decode().strip()  # Read a line from the Pico
            #print("test")
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

def controlLoop():
	speed_mode = 1
	left_motor_pin = 19
	right_motor_pin = 12
	flag_forward =True
	flag_backward = False
	flag_left = False
	flag_right = False
	flag_up = False
	flag_down = False

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
	
	total_time_up = 8
	total_time_down = 8
	total_time_forward = 8
	total_time_backward = 8
	total_time_right = 8
	total_time_left = 8
	
	#initialisation
	
	movement_functions_ground.initialise_neutral_point(left_motor_pin,right_motor_pin)
	
	#time definitions
	
	if flag_forward: 
		anglesR = angles_forward
		anglesL = angles_forward 
		total_time = total_time_forward 
	elif flag_backward:
		anglesR = angles_backward
		anglesL = angles_forward 
		total_time = total_time_backward
	elif flag_left:
		anglesR = angles_left_rm
		anglesL = angles_left_lm
		total_time = total_time_left
	elif flag_right:
		anglesR = angles_right_rm
		anglesL = angles_right_lm
		total_time = total_time_right 
	elif flag_up:
		anglesR = angles_up
		anglesL = angles_up
		total_time = total_time_up 
	elif flag_down:
		anglesR = angles_down
		anglesL = angles_down
		total_time = total_time_down 
	
	
	time_interval = total_time/len (anglesR)
	
	start_time = time.time()
	setpoint_change_time = start_time
	
	current_setpoint_indexR = 0
	current_setpoint_indexL = 0
	angsetpointR= anglesR[current_setpoint_indexR]
	angsetpointL= anglesL[current_setpoint_indexL]


	
	while True:
		current_time = time.time()
		elapsed_time = current_time-start_time
		
		if flag_forward:
			current_movement = "forward"
			anglesR = angles_forward
			anglesL = angles_forward
			time_interval = total_time_forward/len(angles_forward)
			total_time = total_time_forward
			
		elif flag_backward:
			current_movement = "backward"
			angles = angles_backward
			time_interval = total_time_backward/len(angles_backward)
			total_time = total_time_backward
			
		#elif flag_up:
		#	current_movement = "up"
		#	anglesR = angles_up
		#	anglesL = angles_up
		#	time_interval = total_time_up/len(angles_up)
		#	total_time = total_time_up
			
		#elif flag_down:
		#	current_movement = "down"
		#	anglesR = angles_down
		#	anglesL = angles_down
		#	time_interval = total_time_down/len(angles_down)
		#	total_time = total_time_down
			
		#elif flag_right:
		#	current_movement = "right"
		#	anglesR = angles_right_rm
		#	anglesL = angles_right_rm
		#	time_interval = total_time_right/len(angles_right)
		#	total_time = total_time_right
			
		#elif flag_left:
		#	current_movement = "left"
		#	anglesR = angles_left_rm
		#	anglesL = angles_left_rm
		#	time_interval = total_time_left/len(angles_left)
		#	total_time = total_time_left
			
		if current_time - setpoint_change_time >= time_interval:
			
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
	
	       



t1 = threading.Thread(target=get_encoder_data)
t1.start()
t2 = threading.Thread(target=controlLoop)
t2.start()
	#t3 = Process(target=get_heading)
	#t3.start()
	



