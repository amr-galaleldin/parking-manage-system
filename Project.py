import cv2
import numpy as np
import pickle
from flask import Flask, request




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

def predict():
    cap = cv2.VideoCapture('rtsp://admin:LJJRLI@193.227.12.175:554')
    posList = 0
    with open('carParkPos', 'rb') as f:
        posList = pickle.load(f)

    for i in range(1):
            _, img = cap.read()
           
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (3, 3), 1)
            Thre = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
            blur = cv2.medianBlur(Thre, 5)
            kernel = np.ones((3, 3), np.uint8)
            dilate = cv2.dilate(blur, kernel, iterations=1)
            predictt = check(imgPro=dilate, posList=posList)
    return "ااااااااااااااااااااااااااhelllo"




app = Flask(__name__)


@app.route('/parking', methods=["GET"])
def parking():
    return predict()

if __name__ == '__main__':
    app.run(port=5000)
