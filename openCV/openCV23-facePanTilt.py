import cv2
print(cv2.__version__)

import numpy as np

import Adafruit_PCA9685
import time

## init servo motor

## init the pca9685 using desired address/or bus
pwm = Adafruit_PCA9685.PCA9685(address = 0x40, busnum = 1)

down_min = 150 # min pulse length
down_max = 600 # max pulse length
down_mid = 300 # init pos of camera


up_min = 450 # min pulse length
up_max = 650 # max pulse length
up_mid = 550 # init pos of camera

pan = down_mid
tilt = up_mid

## set frequency
pwm.set_pwm_freq(60)

pwm.set_pwm(1,0,up_mid)
pwm.set_pwm(0,0,down_mid)


## want to keep this aspect ratio
## display width/height
dispW=640
dispH=480

## if not 4 camera will be upside down, or horizontally flipped 
flip = 2

## laucnhes g streamer nvarguscamerasrc
## Don't want to run at full full fps as camera can't handle it
## BGR is blue green red
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

## camera is now ready to run
cam = cv2.VideoCapture(camSet)

## so can pull res if decide to change later
width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

## import the face cascade model
face_cascade=cv2.CascadeClassifier('/home/nvidia/Desktop/py-projects/cascade/face.xml')

## import the eye cascade model
eye_cascade=cv2.CascadeClassifier('/home/nvidia/Desktop/py-projects/cascade/eye.xml')

while True:
    ## ret allows creating the var
    ret, frame=cam.read()

    ##convert to grey as less computatial power
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2)

        xCent= x+w/2
        yCent= y+h/2
        errorPan =xCent-dispW/2
        errorTilt = yCent-dispH/2

        ## only move if error is greater that 15
        if abs(errorPan) > 15:
             pan -= int(round(errorPan/30))

        ## as tilt is inverted in real life for me   
        if(abs(errorTilt) > 15):
             tilt += int(round(errorTilt/30))

        if(tilt > up_max):
             tilt = up_max
             print('tilt out of range')
            
        if(tilt < up_min):
             tilt = up_min
             print('tilt out of range')
            
        if(pan > down_max):
             pan = down_max
             print('pan out of range')

        if(tilt < down_min):
             pan = down_min
             print('pan out of range') 

        pwm.set_pwm(1,0,tilt)
        pwm.set_pwm(0,0,pan)
        ## only want to move servo based on largest object not noise

              # To find eyes, we only want to search in the face
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes=eye_cascade.detectMultiScale(roi_gray)

        for(xEye, yEye, wEye, hEye) in eyes:
            cv2.circle(roi_color, (int(xEye+wEye/2),int(yEye+hEye/2)), 7, (255,0,0),-1)
            cv2.circle(roi_color, (int(xEye+wEye/2),int(yEye+hEye/2)), 3, (0,255,0),-1)

        break

    cv2.imshow('piCam', frame)
    cv2.moveWindow('piCam', 0, 0)

    ## checks every ms to see if key is pressed
    if cv2.waitKey(1) ==ord('q'):
        break
## need to release camera otherwise will still run
cam.release()
cv2.destroyAllWindows()