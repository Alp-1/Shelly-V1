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
c1 = threading.Condition()

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
	flag_forward =True
	right_motor_pin = 12
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
		if speed_mode == 1:
			#print(self.flag_forward,self.flag_stop,self.flag_back,self.flag_left,self.flag_right)
			if flag_forward == True :
				 
				 #movement_functions_ground.set_heading(global_heading) 
				 movement_functions.forward(left_motor_pin,right_motor_pin,angle1,angle2,angsetpoint1,angsetpoint2)
			else:    
				 movement_functions_ground.stop_motion(left_motor_pin,right_motor_pin)
	       

	#get_angular_velocity()
t1 = Process(target=get_encoder_data())
t1.start()
t2 = Process(target=controlLoop())
t2.start()
	#t3 = Process(target=get_heading)
	#t3.start()
	



