from flask import Flask, request, jsonify
from flask_cors import CORS
import websockets
import asyncio
import cv2, base64
import threading
c = threading.Condition()
size = ['960','312']

cap = cv2.VideoCapture(0)

while cap.isOpened():
    _, frame = cap.read()

    c.acquire()
    print(frame)
    frame = cv2.resize(frame, (int(size[0]),int(size[1])))
    print(size)
    c.release()

    encoded = cv2.imencode('.jpg', frame)[1]

    #data = str(base64.b64encode(encoded))
    #data = data[2:len(data)-1]

    #await websocket.send(data)

    cv2.imshow("Transimission", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()