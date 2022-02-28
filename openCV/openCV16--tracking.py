import cv2
print(cv2.__version__)

import numpy as np

def nothing(x):
    pass

cv2.namedWindow('Trackbars')
cv2.moveWindow('Trackbars', 1320, 0)

cv2.createTrackbar('hueLower', 'Trackbars', 50, 179, nothing)
cv2.createTrackbar('hueHigher', 'Trackbars', 100, 179, nothing)
cv2.createTrackbar('satLow', 'Trackbars', 100, 255, nothing)
cv2.createTrackbar('satHigh', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('valLow', 'Trackbars', 100, 255, nothing)
cv2.createTrackbar('valHigh', 'Trackbars', 255, 255, nothing)

## want to keep this aspect ratio
## display width/height
dispW=1280
dispH=960

## if not 4 camera will be upside down, or horizontally flipped 
flip = 4

## laucnhes g streamer nvarguscamerasrc
## Don't want to run at full full fps as camera can't handle it
## BGR is blue green red
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

## camera is now ready to run
cam = cv2.VideoCapture(camSet)

while True:
    ## ret allows creating the var
    # #frame will get the last picture from the camera
    ret, frame=cam.read()
    frame = cv2.imread('smarties.png')
    ## Grabbing a frame and then showing the frame
    cv2.imshow('piCam', frame)
    cv2.moveWindow('piCam', 0, 0)

    ## Hard to track RGB, so convert it
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hueLow = cv2.getTrackbarPos('hueLower', 'Trackbars')
    hueUp = cv2.getTrackbarPos('hueHigher', 'Trackbars')

    Ls = cv2.getTrackbarPos('satLow', 'Trackbars')
    Us = cv2.getTrackbarPos('satHigh', 'Trackbars')

    Lv = cv2.getTrackbarPos('valLow', 'Trackbars')
    Uv = cv2.getTrackbarPos('valHigh', 'Trackbars')

    ## lower bound
    l_b = np.array([hueLow, Ls, Lv])
    u_b = np.array([hueUp, Us, Uv])

    ## Only want the smarties
    FGmask = cv2.inRange(hsv, l_b, u_b)
    cv2.imshow('FGmask', FGmask)
    cv2.moveWindow('FGmask', 0, 410)

    FG = cv2.bitwise_and(frame,frame, mask=FGmask)
    cv2.imshow('FG', FG)
    cv2.moveWindow('FG', 480, 0)
    ## checks every ms to see if key is pressed
    if cv2.waitKey(1) ==ord('q'):
        break
## need to release camera otherwise will still run
cam.release()
cv2.destroyAllWindows()