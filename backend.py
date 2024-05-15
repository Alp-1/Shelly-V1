from flask import Flask, request, jsonify
from flask_cors import CORS
import websockets
import asyncio
import cv2, base64
from threading import *
import time
from picamera2 import Picamera2
from control1 import Controller
import pigpio
import subprocess
from multiprocessing import Process, Value
import sys
import RPi.GPIO as GPIO
from functools import partial
GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.IN, pull_up_down = GPIO.PUD_UP)

def checkSwitch():
    while True:
        if GPIO.input(25) == 0:
            break
    subprocess.call(['sh','./script.sh'])
    sys.exit("Resetting")
    
pi = pigpio.pi()

class SizeError(Exception):
    ...
    pass

mode = 2
size = 0
stop=False
previous = ""
app = Flask(__name__)
CORS(app)

cam = Picamera2()
cam2_config = cam.create_video_configuration(main={"size": (320, 240), "format": "XRGB8888"},controls={'FrameRate': 5})
cam.configure(cam2_config)
jpeg_quality = 75

@app.route('/water', methods = ['GET'])
def water_func():
    # Once command generation is complete, go through and apply each command in series
    # Record all video whilst underwater
    # Record log of events whilst underwater
    global mode
    global robotController


    if mode != 2:
        mode = 2
        robotController.mode=2
    
    if 'commands' in request.args:
        array = request.args['commands'].split(',')
        newArr = []
        for x in range(0,len(array)/2):
            newArr.append(array[x*2],array[x*2+1])
        
        robotController.mission_array = mission_array
        robotController.start_mission = True

    return str(mode)

@app.route('/land', methods = ['GET'])
def land_func():
    # Get video stream frames and send data over network - maybe use websocket communication
    # Receive control commands from flutter and apply them appropriately
    global mode
    global robotController
    global size
    if mode != 1:
        mode = 1
        robotController.mode=1
    
    if 'size' in request.args:
        size = int(request.args['size'].split(',')[0])

    if 'query' in request.args:
        print(request.args['query'])
        if request.args['query'] == "forward":
            robotController.start = True
            robotController.flag_stop = False
            robotController.flag_forward = True
            
        elif request.args['query'] == "backward":
            robotController.start = True
            robotController.flag_stop = False
            robotController.flag_back = True
            
        elif request.args['query'] == "left":
            robotController.start = True
            robotController.flag_stop = False
            robotController.flag_left = True
            
        elif request.args['query'] == "right":
            robotController.start = True
            robotController.flag_stop = False
            robotController.flag_right = True
        
        elif request.args['query'] == "stop":
            robotController.flag_stop = True
            robotController.flag_forward = False
            robotController.flag_back = False
            robotController.flag_left = False
            robotController.flag_right = False
            
    return str(mode)

@app.route('/settings', methods = ['GET'])
def settings_func():
    # Once command generation is complete, go through and apply each command in series
    # Record all video whilst underwater
    # Record log of events whilst underwater
    global mode
    global robotController
    global jpeg_quality
    global cam
    print(cam.controls)
    if 'quality' in request.args:
        jpeg_quality = int(request.args['quality'])
        print(jpeg_quality)
    if 'exposure' in request.args:
        print(request.args['exposure'])
        cam.set_controls({'ExposureValue': float(request.args['exposure'])})
    if 'rightTrim' in request.args:
        robotController.rightTrim = float(request.args['rightTrim'])
    if 'leftTrim' in request.args:
        robotController.leftTrim = float(request.args['leftTrim'])
    if 'speed' in request.args:
        robotController.speed_mode = int(request.args['speed'])
    if 'brightness' in request.args:
        print(request.args['brightness'])
        cam.set_controls({'Brightness': float(request.args['brightness'])})
    if mode != 3:
        mode = 3
        robotController.mode=3
    return str(mode)

    
def inter():
    Process(app.run(host='robot.local', port=5000))
    


async def transmit(websocket,path):
    global size
    global mode
    global stop
    global cam
    global jpeg_quality

    print("Client Connected !")
    
    cam.start()
    
    try :
        videoSize = [size, size]

        if mode > 1:
            onPage = False
        else:
            onPage = True
        
        if videoSize[0] == 0 or videoSize[1] == 0:
            raise SizeError
        
        while onPage and not stop:
            frame = cam.capture_array()

            if frame is not None:
                frame = cv2.resize(frame, (videoSize[0], videoSize[1]))
                _, encoded = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
                data = str(base64.b64encode(encoded))
                data = data[2:len(data)-1]
                await websocket.send(data)
            await asyncio.sleep(0.001)

            if mode > 1:
                onPage = False
            else:
                onPage = True

        cam.stop()

    except SizeError:
        print("Image size not specified")
        cam.stop()

    except:
        print("Client Disconnected !")
        cam.stop()

def liveFeed():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(transmit, host="robot.local", port=5001)
    loop.run_until_complete(start_server)
    loop.run_forever()

port = 5001

robotController = Controller()
t1 = Thread(target=inter)
t1.daemon = True
t1.start()
liveFeed()
#t3 = Thread(target=checkSwitch())
#t3.daemon = True
#t3.start()
        






