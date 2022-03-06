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
up_max = 600 # max pulse length
up_mid = 500 # init pos of camera

pan = down_mid
tilt = up_mid

## set frequency
pwm.set_pwm_freq(60)

pwm.set_pwm(1,0,up_mid)
pwm.set_pwm(0,0,down_mid)


def nothing(x):
    pass

cv2.namedWindow('Trackbars')
cv2.moveWindow('Trackbars', 1320, 0)

cv2.createTrackbar('hueLower', 'Trackbars', 170, 179, nothing)
cv2.createTrackbar('hueHigher', 'Trackbars', 179, 179, nothing)

## need more specific to track all red

cv2.createTrackbar('hue2Lower', 'Trackbars', 0, 179, nothing)
cv2.createTrackbar('hue2Higher', 'Trackbars', 10, 179, nothing)

cv2.createTrackbar('satLow', 'Trackbars', 99, 255, nothing)
cv2.createTrackbar('satHigh', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('valLow', 'Trackbars', 96, 255, nothing)
cv2.createTrackbar('valHigh', 'Trackbars', 255, 255, nothing)

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

while True:
    ## ret allows creating the var
    # #frame will get the last picture from the camera
    ret, frame=cam.read()
    ## If want to edit smarties png for testing
    ##frame = cv2.imread('smarties.png')
    ## Grabbing a frame and then showing the frame

    ## Hard to track RGB, so convert it
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hueLow = cv2.getTrackbarPos('hueLower', 'Trackbars')
    hueUp = cv2.getTrackbarPos('hueHigher', 'Trackbars')

    hue2Low = cv2.getTrackbarPos('hue2Lower', 'Trackbars')
    hue2Up = cv2.getTrackbarPos('hue2Higher', 'Trackbars')

    Ls = cv2.getTrackbarPos('satLow', 'Trackbars')
    Us = cv2.getTrackbarPos('satHigh', 'Trackbars')

    Lv = cv2.getTrackbarPos('valLow', 'Trackbars')
    Uv = cv2.getTrackbarPos('valHigh', 'Trackbars')

    ## lower bound
    l_b = np.array([hueLow, Ls, Lv])
    u_b = np.array([hueUp, Us, Uv])

    l_b2 = np.array([hue2Low, Ls, Lv])
    u_b2 = np.array([hue2Up, Us, Uv])

    ## Only want the smarties
    FGmask = cv2.inRange(hsv, l_b, u_b)
    FGmask2 = cv2.inRange(hsv, l_b2, u_b2)
    FGmaskComp = cv2.add(FGmask, FGmask2)

    cv2.imshow('FGmaskComp', FGmaskComp)
    cv2.moveWindow('FGmaskComp', 0, 500)

    ## find the points on the image
    ## use the mask to genearte contours
    contours,_ = cv2.findContours(FGmaskComp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ## show the bigest contours first
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)

    ## want to be able to track more than one object of interst
    for cnt in contours:
        area = cv2.contourArea(cnt)
        (x,y,w,h) = cv2.boundingRect(cnt)
        if area >50: 
            ## expected an array
            ##cv2.drawContours(frame, [cnt], 0, (255,0,0), 3)
            cv2.rectangle(frame,(x,y), (x+w, y+h), (255,0,0), 3)
            ## width /2 to find center
            objX = x+w/2
            ## to find center height / 2
            objY = y+h/2
            ## How far we are off in x axis
            ## need to find centre of screen hence get width
            errorX = objX - width/2
            errorY = objY - height/2

            ## only move if error is greater that 15
            if(abs(errorX) > 15):
                pan -= int(round(errorX/50))
            ## as tilt is inverted in real life for me   
            if(abs(errorY) > 15):
                tilt += int(round(errorY/50))

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
            break

    ## 0 draw only one conture
    #cv2.drawContours(frame, contours, 0, (255,0,0),3)

    cv2.imshow('piCam', frame)
    cv2.moveWindow('piCam', 0, 0)

    ## checks every ms to see if key is pressed
    if cv2.waitKey(1) ==ord('q'):
        break
## need to release camera otherwise will still run
cam.release()
cv2.destroyAllWindows()