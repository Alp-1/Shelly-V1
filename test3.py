import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.IN, pull_up_down = GPIO.PUD_UP)
while True:
    print(GPIO.input(25))
