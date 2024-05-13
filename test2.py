from flask import Flask, request, jsonify
from flask_cors import CORS
import websockets
import asyncio
import cv2, base64
import threading
import time
from picamera2 import Picamera2
from control1 import Controller
import pigpio

robotController = Controller()
def alternate():
	while True:
		print("Stop")
		robotController.flag_stop = False
		robotController.flag_forward = True

		time.sleep(5)
		print("Go")
		robotController.flag_stop = True
		robotController.flag_forward = False
		time.sleep(5)

#t1 = threading.Thread(target=alternate, name="t1",args=())
#t1.start()
robotController.controlLoop()






