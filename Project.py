import cv2
import numpy as np
import pickle
from flask import Flask
# from flask_socketio import SocketIO



rectW,rectH=107,48



def check(imgPro,posList):
    spaceCount=0
    for pos in posList:
        x,y=pos
        crop=imgPro[y:y+rectH,x:x+rectW]
        count=cv2.countNonZero(crop)
        if count<900:
            spaceCount+=1
        #     color=(0,255,0)
        #     thick=5
        # else:
        #     color=(0,0,255)
        #     thick=2

    #     cv2.rectangle(img,pos,(x+rectW,y+rectH),color,thick)
    # cv2.rectangle(img,(45,30),(250,75),(180,0,180),-1)
    # cv2.putText(img,f'Free: {spaceCount}/{len(posList)}',(50,60),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),2)
    return {'capacity':len(posList),'busy':spaceCount}


def predict():
 cap=cv2.VideoCapture('new1.mp4')
 posList=0
 with open('carParkPos','rb') as f:
    posList=pickle.load(f)
 frame_counter = 0
 for i in range(1):
    _,img=cap.read()
    if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        frame_counter = 0 #Or whatever as long as it is the same as next line
        cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 0)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(3,3),1)
    Thre=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    blur=cv2.medianBlur(Thre,5)
    kernel=np.ones((3,3),np.uint8)
    dilate=cv2.dilate(blur,kernel,iterations=1)
    predictt= check(imgPro=dilate,posList=posList)

    # cv2.imshow("Image",img)
    # cv2.waitKey(10)

 return predictt



app = Flask(__name__)


@app.route('/parking')
def emotion():

  return predict()


if __name__ == '__main__':
   
    app.run( port=5000,debug=True)
