import cv2
import numpy as np
print(cv2.__version__)

## creating a matrix with 480 rows 640 colums and one colour for grayscale
img1 = np.zeros((480, 640,1), np.uint8)

## turning half white
img1[0:480, 0:320] = [255]

img2 = np.zeros((480, 640, 1), np.uint8)
img2[190:290, 270:370] = [255] 

## only show white etc if both are white
bitAnd = cv2.bitwise_and(img1, img2)

## only white if either are white
bitOr = cv2.bitwise_or(img1, img2)

## opposite of or. so if 11 or oo returns 0
## so only white if either are white
bitXor = cv2.bitwise_xor(img1, img2)

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
    ## Grabbing a frame and then showing the frame

    cv2.imshow('img1', img1)
    cv2.moveWindow('img1', 0, 500)

    cv2.imshow('img2', img2)
    cv2.moveWindow('img2', 700, 500)


    cv2.imshow('AND', bitAnd)
    cv2.moveWindow('AND', 700, 1000)

    cv2.imshow('OR', bitOr)
    cv2.moveWindow('OR', 1340, 0)
    
    ## shows on the frame where it is only white
    #frame=cv2.bitwise_and(frame, frame, mask=img1)
    #cv2.imshow('piCam', frame)
    ## checks every ms to see if key is pressed
    if cv2.waitKey(1) ==ord('q'):
        break
## need to release camera otherwise will still run
cam.release()
cv2.destroyAllWindows()