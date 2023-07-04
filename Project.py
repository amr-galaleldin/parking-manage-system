
import gevent.monkey

gevent.monkey.patch_all()


import cv2
import numpy as np
import pickle
from flask import Flask, request
from flask_socketio import SocketIO




rectW, rectH = 107, 48

def check(imgPro, posList):
    spaceCount = 0
    for pos in posList:
        x, y = pos
        crop = imgPro[y:y+rectH, x:x+rectW]
        count = cv2.countNonZero(crop)
        if count < 900:
            spaceCount += 1
    return {'capacity': len(posList), 'freespaces': spaceCount}

def predict(num):
    cap = cv2.VideoCapture('new1.mp4')
    posList = 0
    with open('carParkPos', 'rb') as f:
        posList = pickle.load(f)
    frame_counter = 0
    if num == 0:
        while True:
            _, img = cap.read()
            if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                break
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (3, 3), 1)
            Thre = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
            blur = cv2.medianBlur(Thre, 5)
            kernel = np.ones((3, 3), np.uint8)
            dilate = cv2.dilate(blur, kernel, iterations=1)
            predictt = check(imgPro=dilate, posList=posList)
            socketio.emit('predict',{"predictt":"cat"} )
            gevent.sleep(0)
            frame_counter+=1
    else:
        for i in range(1):
            _, img = cap.read()
            if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                break
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (3, 3), 1)
            Thre = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
            blur = cv2.medianBlur(Thre, 5)
            kernel = np.ones((3, 3), np.uint8)
            dilate = cv2.dilate(blur, kernel, iterations=1)
            predictt = check(imgPro=dilate, posList=posList)
        return predictt

app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent')



def capture_frames():
    predict(0)

@socketio.on('connect')
def on_connect():
    socketio.start_background_task(capture_frames)

@app.route('/parking', methods=["GET"])
def parking():
    # return predict(1)
    return "hello world"

if __name__ == '__main__':
    socketio.run(app,port=5000)
