import cv2
import numpy as np
import pickle
from flask import Flask,request
from flask_socketio import SocketIO
import eventlet



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
    return {'capacity':len(posList),'freespaces':spaceCount}



# mother method we will trigger

def predict(num):
 
  cap=cv2.VideoCapture('new1.mp4')
#   cap.set(cv2.CAP_PROP_POS_FRAMES, 300)
  posList=0
  with open('carParkPos','rb') as f:
    posList=pickle.load(f)
  frame_counter = 0
  if num == 0:
   while True:
    _,img=cap.read()
    if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        # frame_counter = 0 #Or whatever as long as it is the same as next line
        # cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        break
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(3,3),1)
    Thre=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    blur=cv2.medianBlur(Thre,5)
    kernel=np.ones((3,3),np.uint8)
    dilate=cv2.dilate(blur,kernel,iterations=1)
    predictt= check(imgPro=dilate,posList=posList)
   

    # cv2.imshow("Image",img)
    # cv2.waitKey(10)

    eventlet.sleep(0)
   
    socketio.emit('predict', predictt)
  else :
      for i in range(1):
       _,img=cap.read()
       if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        # frame_counter = 0 #Or whatever as long as it is the same as next line
        # cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
           break
       gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
       blur=cv2.GaussianBlur(gray,(3,3),1)
       Thre=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
       blur=cv2.medianBlur(Thre,5)
       kernel=np.ones((3,3),np.uint8)
       dilate=cv2.dilate(blur,kernel,iterations=1)
       predictt= check(imgPro=dilate,posList=posList)
      return predictt
     
    

#  setup socket and rest api







app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

eventlet.monkey_patch()

def capture_frames():
  

    predict(0)

@socketio.on('connect')
def on_connect():
    socketio.start_background_task(capture_frames)



@app.route('/parking',methods=["GET",'POST'])


def emotion():
  if  request.method=="POST":

   # return predict(1)
      return "hello world"



if __name__ == '__main__':
    socketio.run(app,debug=True)


















































































# import cv2
# import numpy as np
# import pickle
# from flask import Flask, request
# from flask_socketio import SocketIO
# import eventlet

# rectW, rectH = 107, 48

# def check(imgPro, posList):
#     spaceCount = 0
#     for pos in posList:
#         x, y = pos
#         crop = imgPro[y:y+rectH, x:x+rectW]
#         count = cv2.countNonZero(crop)
#         if count < 900:
#             spaceCount += 1

#     return {'capacity': len(posList), 'busy': spaceCount}

# predict_task = {}

# def predict(num, sid):
#     cap = cv2.VideoCapture('new1.mp4')
#     posList = 0
#     with open('carParkPos', 'rb') as f:
#         posList = pickle.load(f)
#     frame_counter = 0
#     if num == 0:
#         predict_task[sid] = socketio.start_background_task(predict, 0, sid)
#         while True:
#             _, img = cap.read()
#             if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
#                 break
#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             blur = cv2.GaussianBlur(gray, (3, 3), 1)
#             Thre = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
#             blur = cv2.medianBlur(Thre, 5)
#             kernel = np.ones((3, 3), np.uint8)
#             dilate = cv2.dilate(blur, kernel, iterations=1)
#             predictt = check(imgPro=dilate, posList=posList)
#             print("00000")
#             socketio.emit('predict', predictt, room=sid)
#             eventlet.sleep(0)
#     else:
#         predict_task[sid] = socketio.start_background_task(predict, 1, sid)
#         for i in range(1):
#             _, img = cap.read()
#             if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
#                 break
#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             blur = cv2.GaussianBlur(gray, (3, 3), 1)
#             Thre = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
#             blur = cv2.medianBlur(Thre, 5)
#             kernel = np.ones((3, 3), np.uint8)
#             dilate = cv2.dilate(blur, kernel, iterations=1)
#             predictt = check(imgPro=dilate, posList=posList)
#         return predictt

# def stop_predict(sid):
#     if sid in predict_task:
#         socketio.stop_background_task(predict_task[sid])
#         del predict_task[sid]

# app = Flask(__name__)
# socketio = SocketIO(app, async_mode='eventlet')

# eventlet.monkey_patch()

# clients = {}

# def capture_frames(sid):
#     clients[sid] = True
#     predict(0, sid)

# @app.route('/parking')
# def parking():
#     sid = request.sid
#     return predict(1, sid)

# @socketio.on('connect')
# def on_connect():
#     sid = request.sid
#     socketio.start_background_task(capture_frames, sid)

# @socketio.on('disconnect')
# def on_disconnect():
#     sid = request.sid
#     if sid in clients:
#         del clients[sid]
#         stop_predict(sid)

# if __name__ == '__main__':
#     socketio.run(app, port=3000, debug=True)
