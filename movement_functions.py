from simple_pid import PID
import pigpio
import time
import numpy as np

pi = pigpio.pi()


target_setpoint = -0.02 # get this from ui

pid_left= PID(1,0.1,0.05, setpoint = target_setpoint)
pid_right= PID(1,0.1,0.05, setpoint = target_setpoint)
pid_forward_flop= PID(0.4,0.00001,0.001, 0)
pid_forward_flop.sample_time = 0.000001
pid_forward_flop.output_limits = (-400,400)

pid_back= PID(1,0.1,0.05, setpoint = target_setpoint)

def map_to_value(v1, center_pwm):
    amplitude = 300
    start1, end1 = -400,400
    dead_zone_start, dead_zone_end = 1500,1630
    start2_low, end2_low =600, dead_zone_start
    start2_high, end2_high = dead_zone_end, 2500
    #mapped1 = start2 + (end2-start2)*(v1-start1)/(end1-start1)
    #mapped2 = start2 + (end2-start2)*(v2-start2)/(end-start1)
    
    if v1 < 0:
        base_mapped = start2_low + (end2_low - start2_low)* ((v1-start1) / (0 - start1))
    else:
        base_mapped = start2_high + (end2_high - start2_high)* ((v1-0) / (end1 - 0))
        
    t= time.time()%10
    cosine_adjustment = amplitude*np.cos(2*np.pi*0.5*t) # 0.5 freq
    pwm_value = center_pwm + cosine_adjustment
    pwm_value = max(min(pwm_value,base_mapped), 600, min(pwm_value,base_mapped,2500))
    
    return int(pwm_value)    

def calculate_pwm(t,frequency=0.5,min_pwm=600,max_pwm=2500):
    cosine_value = np.cos(2*np.pi*frequency*t)
    normalized_cosine = (cosine_value +1)/2
    pwm_value = min_pwm+normalized_cosine*(max_pwm - min_pwm)
    return pwm_value
    
def stop_motion(left_motor_pin,right_motor_pin):
    pi.set_servo_pulsewidth(left_motor_pin, 1550)
    pi.set_servo_pulsewidth(right_motor_pin, 1550)
    
def forward(left_motor_pin,right_motor_pin,current_angle1,current_angle2,set1,set2):
    #angle controller
    err1=int(set1-current_angle1)
    print("err",err1)
    pid_forward_flop.setpoint = int(set1)
    print("set1",pid_forward_flop.setpoint)
    print("angle1",current_angle1)
    print("angle2",current_angle2)
    
    if abs(err1) <5:
        stop_motion(left_motor_pin,right_motor_pin)
    else:
        control_action = pid_forward_flop(int(current_angle1))
        center_pwm=1550 + control_action
        a = map_to_value(control_action,center_pwm)
        #print("set1",set1)
        print("PMW",a)
    #pwm
        pi.set_servo_pulsewidth(right_motor_pin, a)
        
    
# def forward(left_motor_pin,right_motor_pin,current_angle1,current_angle2,set1,set2):
    # #angle controller
    # err1=int(set1-current_angle1)
    # print("err",err1)
    # pid_forward_flop.setpoint = int(set1)
    # print("set1",pid_forward_flop.setpoint)
    # print("angle1",current_angle1)
    # print("angle2",current_angle2)
    
    # if abs(err1) <5:
        # stop_motion(left_motor_pin,right_motor_pin)
    # else:
        # control_action = pid_forward_flop(int(current_angle1))
        # a = map_to_value(control_action)
        # #print("set1",set1)
        # print("PMW",a)
    # #pwm
        # pi.set_servo_pulsewidth(right_motor_pin, a)
        
        
        
	
# def backward(current_speed,flag_forward,flag_forward_stop,flag_back,flag_back_stop,flag_left,flag_left_stop,flag_right,flag_right_stop):
    # flag_forward = flag_forward
    # flag_forward_stop = flag_forward_stop
    # flag_left = flag_left
    # flag_left_stop = flag_left_stop
    # flag_right = flag_right
    # flag_right_stop = flag_right_stop
    # flag_back = flag_back
    # flag_back_stop = flag_back_stop
    # if flag_back == True and flag_back_stop == False:	
     # output = pid_back(current_speed)
     # pi.set_servo_pulsewidth(left_motor_pin, output)
     # pi.set_servo_pulsewidth(right_motor_pin, output)
    # elif flag_back == False and flag_back_stop == True:
     # stop_motion()
    # elif flag_back == True and (flag_forward == True or flag_left == True or flag_right == True):
     # print ("Too many inputs, give one at a time!")
    # else:
     # print ("Exception on forward function, Stopping.")
     # stop_motion()
    
# def left(current_speed,flag_forward,flag_forward_stop,flag_back,flag_back_stop,flag_left,flag_left_stop,flag_right,flag_right_stop):
    # flag_forward = flag_forward
    # flag_forward_stop = flag_forward_stop
    # flag_left = flag_left
    # flag_left_stop = flag_left_stop
    # flag_right = flag_right
    # flag_right_stop = flag_right_stop
    # flag_back = flag_back
    # flag_back_stop = flag_back_stop
    # if flag_left == True and flag_left_stop == False:	
     # output = pid_left(current_speed)
     # pi.set_servo_pulsewidth(left_motor_pin, output)
     # pi.set_servo_pulsewidth(right_motor_pin, output)
     # sleep(0.5)
    # elif flag_left == False and flag_left_stop == True:
     # stop_motion()
    # elif flag_left == True and (flag_back == True or flag_forward == True or flag_right == True):
     # print ("Too many inputs, give one at a time!")
    # else:
     # print ("Exception on left function, Stopping.")
     # stop_motion()
	
# def right(current_speed,flag_forward,flag_forward_stop,flag_back,flag_back_stop,flag_left,flag_left_stop,flag_right,flag_right_stop):
    # flag_forward = flag_forward
    # flag_forward_stop = flag_forward_stop
    # flag_left = flag_left
    # flag_left_stop = flag_left_stop
    # flag_right = flag_right
    # flag_right_stop = flag_right_stop
    # flag_back = flag_back
    # flag_back_stop = flag_back_stop
    # if flag_right == True and flag_right_stop == False:	
     # output = pid_right(current_speed)
     # pi.set_servo_pulsewidth(left_motor_pin, output)
     # pi.set_servo_pulsewidth(right_motor_pin, output)
     # sleep(0.5)
    # elif flag_right == False and flag_right_stop == True:
     # stop_motion()
    # elif flag_right == True and (flag_back == True or flag_left == True or flag_forward == True):
     # print ("Too many inputs, give one at a time!")
    # else:
     # print ("Exception on forward function, Stopping.")
     # stop_motion()
     
     
## HardCoded Functions:
def forward_hard(left_motor_pin,right_motor_pin,speed_mode):

    if speed_mode == 1: #Slow
         
     while 1:
      temppwm = calculate_pwm(time.time())    
      pi.set_servo_pulsewidth(left_motor_pin, temppwm)
      pi.set_servo_pulsewidth(right_motor_pin, temppwm)

    
    elif speed_mode == 2: #Medium
     pi.set_servo_pulsewidth(left_motor_pin, 1350)
     pi.set_servo_pulsewidth(right_motor_pin, 1750)

        
    elif speed_mode == 3: #Fast
     pi.set_servo_pulsewidth(left_motor_pin, 1250)
     pi.set_servo_pulsewidth(right_motor_pin, 1950)
     
def backward_hard(left_motor_pin,right_motor_pin,speed_mode):

    if speed_mode == 1: #Slow
     pi.set_servo_pulsewidth(left_motor_pin, 1650)
     pi.set_servo_pulsewidth(right_motor_pin, 1450)

    
    elif speed_mode == 2: #Medium
     pi.set_servo_pulsewidth(left_motor_pin, 1750)
     pi.set_servo_pulsewidth(right_motor_pin, 1350)

        
    elif speed_mode == 3: #Fast
     pi.set_servo_pulsewidth(left_motor_pin, 1950)
     pi.set_servo_pulsewidth(right_motor_pin, 1250)
    
def left_hard(left_motor_pin,right_motor_pin,speed_mode):

    if speed_mode == 1: #Slow
     pi.set_servo_pulsewidth(left_motor_pin, 1650)
     pi.set_servo_pulsewidth(right_motor_pin, 1650)

    
    elif speed_mode == 2: #Medium
     pi.set_servo_pulsewidth(left_motor_pin, 1050)
     pi.set_servo_pulsewidth(right_motor_pin, 1050)

        
    elif speed_mode == 3: #Fast
     pi.set_servo_pulsewidth(left_motor_pin, 600)
     pi.set_servo_pulsewidth(right_motor_pin, 600)

def right_hard(left_motor_pin,right_motor_pin,speed_mode):

    if speed_mode == 1: #Slow
     pi.set_servo_pulsewidth(left_motor_pin, 1450)
     pi.set_servo_pulsewidth(right_motor_pin, 1450)

    
    elif speed_mode == 2: #Medium
     pi.set_servo_pulsewidth(left_motor_pin, 1050)
     pi.set_servo_pulsewidth(right_motor_pin, 1050)

        
    elif speed_mode == 3: #Fast
     pi.set_servo_pulsewidth(left_motor_pin, 600)
     pi.set_servo_pulsewidth(right_motor_pin, 600)
