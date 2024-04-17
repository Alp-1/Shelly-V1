from flask import Flask, request, jsonify
from flask_cors import CORS
import websockets
import asyncio
import cv2, base64
import threading

app = Flask(__name__)
CORS(app)

mode = 0

c = threading.Condition()
size = [0,0]


@app.route('/test', methods = ['GET'])
def test_func():
    d = {}
    d['output'] = request.args['query']
    return d

@app.route('/water', methods = ['GET'])
def water_func():
    # Once command generation is complete, go through and apply each command in series
    # Record all video whilst underwater
    # Record log of events whilst underwater
    global mode
    if mode != 2:
        mode = 2
    return str(mode)

@app.route('/land', methods = ['GET'])
def land_func():
    # Get video stream frames and send data over network - maybe use websocket communication
    # Receive control commands from flutter and apply them appropriately
    global size
    global mode

    c.acquire()
    size = request.args['size'].split(',')
    c.release()

    if mode != 1:
        mode = 1
    return str(mode)

@app.route('/settings', methods = ['GET'])
def settings_func():
    # Once command generation is complete, go through and apply each command in series
    # Record all video whilst underwater
    # Record log of events whilst underwater
    global mode
    if mode != 3:
        mode = 3
    return str(mode)


if __name__ == '__main__':
    t1 = threading.Thread(target=app.run, name="t1", args=())
    t1.start()

port = 5001

print("Started server on port : ", port)

async def transmit(websocket, path):
    global size
    print("Client Connected !")
    await websocket.send("Connection Established")
    try :
        # Code here would need to be change (takes webcam video feed instead of desired raspi camera feed)
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            _, frame = cap.read()

            c.acquire()
            print(frame)
            frame = cv2.resize(frame, (size[0],size[1]))
            print(size)
            c.release()

            encoded = cv2.imencode('.jpg', frame)[1]

            data = str(base64.b64encode(encoded))
            data = data[2:len(data)-1]

            await websocket.send(data)

            #cv2.imshow("Transimission", frame)

            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break
        cap.release()
    #except websockets.connection.ConnectionClosed as e:

    except:
        print("Client Disconnected !")
        cap.release()

start_server = websockets.serve(transmit, host="127.0.0.1", port=port)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()