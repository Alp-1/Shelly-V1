from simple_pid import PID
import pigpio
import time
import math

pi = pigpio.pi()

trim_l=0
trim_r=0


target_heading = 65
current_heading = 0
pid_heading= PID(0.5,0.1,0.1, setpoint = target_heading)
pid_heading.sample_time = 0.5
pid_heading.output_limits = (-180,180)
pid_heading.error_map
pid_forward_right= PID(0.5,0.1,0.2, setpoint = 1)
pid_forward_left= PID(0.5,0.1,0.2, setpoint =1)
pid_forward_left.output_limits = (1650,2500)
pid_forward_right.output_limits = (1650,2500)
pid_back= PID(1,0.1,0.05, setpoint = target_heading)

def set_heading(heading):
    global current_heading
    current_heading = heading

def set_target(heading):
    global target_heading
    target_heading = heading
    
def mix(rate_of_heading_correction,straight_speed_vector):
    x = rate_of_heading_correction
    y = straight_speed_vector
    #convert to polar
    r = math.hypot(x,y)
    t = math.atan2(y,x)
    #rotate by 45 degrees
    t += math.pi/4
    #map to cartesian
    left = r*math.cos(t)
    right = r*math.sin(t)
    #rescale the new cooardinates
    left = left*math.sqrt(2)
    right = right*math.sqrt(2)
    #clamp to -1/+1
    left = max(-1, min(left,1))
    right = max(-1, min(right,1))
    
    return left,right

def map_to_value(left,right):
    start2,end2 = 600,2500
    mapped1 = start2 + (end2-start2)*(left+1)/2
    mapped2 = start2 + (end2-start2)*(right+1)/2
    return mapped1,mapped2
    
def initialise_neutral_point(left_motor_pin, right_motor_pin):
    pi.set_servo_pulsewidth(left_motor_pin, 1000)
    pi.set_servo_pulsewidth(right_motor_pin, 1000)
    time.sleep(3)
    print("Neutral Setpoint set at 1000")
    # Most likely will add a function for 180 deg phase difference between legs

    
def stop_motion(left_motor_pin, right_motor_pin):
    pi.set_servo_pulsewidth(left_motor_pin, 1550) #(+- 50 deadzone max(600, 2500) (Neutral set at 1550)
    pi.set_servo_pulsewidth(right_motor_pin, 1550)
    
def forward(left_motor_pin,right_motor_pin,speed_mode,rpm1,rpm2,position):
    global current_heading, target_heading
    print(postion)
    #heading_error = target_heading-current_heading
    base_speed= 1550
    if speed_mode == 1: #Slow
     base_speed= 20
     #control_action = pid_heading(heading_error)
     #left,right = mix(control_action,base_speed)
     #pmw_L,pmw_R= map_to_value(left,right)
     #pi.set_servo_pulsewidth(left_motor_pin, 1750)
     #pi.set_servo_pulsewidth(right_motor_pin, 1750)
     #print ("pid response forward",output)
     #print ("last error forward",error)
     
     #print ("heading", current_heading)
     #print ("heading err",heading_error)
     #print ("pm_L",pmw_L)
     #print ("pm_R",pmw_R)

     #pi.set_servo_pulsewidth(left_motor_pin, 1650)
     #pi.set_servo_pulsewidth(right_motor_pin, 1450)
     #print("Going forward")
    
    elif speed_mode == 2: #Medium
     pi.set_servo_pulsewidth(left_motor_pin, 2050)
     pi.set_servo_pulsewidth(right_motor_pin, 2050)
     #print("Going forward")
        
    elif speed_mode == 3: #Fast
     pi.set_servo_pulsewidth(left_motor_pin, 2500)
     pi.set_servo_pulsewidth(right_motor_pin, 2500)
     #print("Going forward")    
    
    else:
        print("invalid speed mode")


  
def backward(left_motor_pin,right_motor_pin,speed_mode,rpm1,rpm2):

    if speed_mode == 1: #Slow
     pi.set_servo_pulsewidth(left_motor_pin, 1250)
     pi.set_servo_pulsewidth(right_motor_pin, 1250)
     #print("Going forward")
    
    elif speed_mode == 2: #Medium
     pi.set_servo_pulsewidth(left_motor_pin, 1050)
     pi.set_servo_pulsewidth(right_motor_pin, 1050)
     #print("Going forward")
        
    elif speed_mode == 3: #Fast
     pi.set_servo_pulsewidth(left_motor_pin, 600)
     pi.set_servo_pulsewidth(right_motor_pin, 600)
     #print("Going forward")    
    
    else:
        print("invalid speed mode")
        

    
def left(left_motor_pin,right_motor_pin,speed_mode,rpm1,rpm2):

    if speed_mode == 1: #Slow
     pi.set_servo_pulsewidth(left_motor_pin, 1850)
     pi.set_servo_pulsewidth(right_motor_pin, 1250)
     print("Going forward")
    
    elif speed_mode == 2: #Medium
     pi.set_servo_pulsewidth(left_motor_pin, 2050)
     pi.set_servo_pulsewidth(right_motor_pin, 1050)
     print("Going forward")
        
    elif speed_mode == 3: #Fast
     pi.set_servo_pulsewidth(left_motor_pin, 2500)
     pi.set_servo_pulsewidth(right_motor_pin, 600)
     print("Going forward")    
    
    else:
        print("invalid speed mode")

	
def right(left_motor_pin,right_motor_pin,speed_mode,rpm1,rpm2):

    if speed_mode == 1: #Slow
     pi.set_servo_pulsewidth(left_motor_pin, 1250)
     pi.set_servo_pulsewidth(right_motor_pin, 1850)
     print("Going forward")
    
    elif speed_mode == 2: #Medium
     pi.set_servo_pulsewidth(left_motor_pin, 1050)
     pi.set_servo_pulsewidth(right_motor_pin, 2050)
     print("Going forward")
        
    elif speed_mode == 3: #Fast
     pi.set_servo_pulsewidth(left_motor_pin, 600)
     pi.set_servo_pulsewidth(right_motor_pin, 2500)
     print("Going forward")    
    
    else:
        print("invalid speed mode")


## HardCoded Functions:
def forward_hard(left_motor_pin,right_motor_pin,speed_mode):

    if speed_mode == 1: #Slow
     pi.set_servo_pulsewidth(left_motor_pin, 1450)
     pi.set_servo_pulsewidth(right_motor_pin, 1650)

    
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


