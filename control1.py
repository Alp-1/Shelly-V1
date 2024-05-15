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
        i=0
        angsetpoint1 = 0
        while True:
            if self.mode == 1:
                #print(self.flag_forward,self.flag_stop,self.flag_back,self.flag_left,self.flag_right)
                if self.flag_forward == True and self.flag_stop == False and self.flag_back == False and self.flag_right == False and self.flag_left==False:

                    if i == 10:
                        angsetpoint1 = 0
                    
                    err1=int(angsetpoint1-angle1)
                    print("err",err1)
                    pid_forward_flop.setpoint = int(angsetpoint1)
                    print("set1",pid_forward_flop.setpoint)
                    print("angle1",angle1)

    
                    if abs(err1) <5:
                        self.pi.set_servo_pulsewidth(12, 1000)
        
                    else:
                        control_action = pid_forward_flop(int(angle1))
                    print("action",control_action) 
                    a = map_to_value(control_action)
                    print("PMW",a)
                    self.pi.set_servo_pulsewidth(12, a)
        
                    #movement_functions.forward(self.left_motor_pin,self.right_motor_pin,angle1,angle2,angsetpoint1)
                    #pid_update(currangle, setpoint)
                    i+=1 
                    print (angsetpoint1)
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
             
# import pigpio
# import threading
# import serial
# from queue import Queue
# import time
# import smbus
# import time
# import math
# from simple_pid import PID
# import movement_functions
# import movement_functions_ground
# from multiprocessing import Process, Value

# # Serial Initialization
# ser = serial.Serial(port='/dev/ttyACM1', baudrate=115200, timeout=1)
# ser1 = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)

# # Globals

# angvel1 = 0
# rpm1 = 0
# angle1 = 0
# angvel2 = 0
# rpm2 = 0
# angle2 = 0
# global_heading = 0

# data_queue = Queue()

# # Function to check if a string is a float
# def is_float(string):
    # try:
        # float(string)
        # return True
    # except ValueError:
        # return False

# # Function to collect serial data
# def collect_serial_data(serial_device, identifier):
    # while True:
        # if serial_device.in_waiting > 0:
            # data = serial_device.readline().decode('utf-8').strip()
            # if data:
                # data_queue.put((identifier, data))

# # Controller class with movement integration
# class Controller:
    # def __init__(self):
        # self.pi = pigpio.pi()
        # if not self.pi.connected:
            # print("No connection to pigpio daemon.")
            # sys.exit()

        # # Motor pins
        # self.left_motor_pin = 19
        # self.right_motor_pin = 12
        # self.pi.set_mode(self.left_motor_pin, pigpio.OUTPUT)
        # self.pi.set_mode(self.right_motor_pin, pigpio.OUTPUT)
        # self.flag_forward = False
        # self.flag_back = False
        # self.flag_left = False
        # self.flag_right = False
        # self.flag_stop = True

        # # Start threads
        # threading.Thread(target=collect_serial_data, args=(ser, 'heading'), daemon=True).start()
        # threading.Thread(target=collect_serial_data, args=(ser1, 'encoder'), daemon=True).start()
        # threading.Thread(target=self.control_loop, daemon=True).start()

    # def control_loop(self):
        # global angvel1, rpm1, angle1, angvel2, rpm2, angle2, global_heading
        # while True:
            # if not data_queue.empty():
                # identifier, data = data_queue.get()
                # if identifier == 'heading' and is_float(data):
                    # global_heading = float(data)
                # elif identifier == 'encoder':
                    # parts = data.split()
                    # if len(parts) == 4:
                        # encoder_id = int(parts[0])
                        # if encoder_id == 1:
                            # angvel1, rpm1, angle1 = float(parts[1]), float(parts[2]), float(parts[3])
                        # elif encoder_id == 2:
                            # angvel2, rpm2, angle2 = float(parts[1]), float(parts[2]), float(parts[3])

            # # Control logic based on flags and sensor readings
            # if self.flag_forward:
                # # Example movement function call
                # movement_functions_ground.forward(self.left_motor_pin, self.right_motor_pin, angle1, angle2)
            # elif self.flag_back:
                # movement_functions_ground.backward_hard(self.left_motor_pin, self.right_motor_pin)
            # elif self.flag_left:
                # movement_functions_ground.left_hard(self.left_motor_pin, self.right_motor_pin)
            # elif self.flag_right:
                # movement_functions_ground.right_hard(self.left_motor_pin, self.right_motor_pin)
            # elif self.flag_stop:
                # movement_functions_ground.stop_motion(self.left_motor_pin, self.right_motor_pin)

            # time.sleep(0.1)  # Sleep to reduce CPU usage

# if __name__ == '__main__':
    # controller = Controller()
    # try:
        # while True:
            # time.sleep(1)
    # except KeyboardInterrupt:
        # print("Program stopped by the user.")
        # sys.exit()

