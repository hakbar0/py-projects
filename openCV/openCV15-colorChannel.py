import cv2
import numpy as np
print(cv2.__version__)

## want to keep this aspect ratio
## display width/height
dispW=640
dispH=480

## if not 4 camera will be upside down, or horizontally flipped 
flip = 4

## laucnhes g streamer nvarguscamerasrc
## Don't want to run at full full fps as camera can't handle it
## BGR is blue green red
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

## camera is now ready to run
cam = cv2.VideoCapture(camSet)

## grayscale image
blank = np.zeros([480, 640, 1], np.uint8)

while True:
    ## ret allows creating the var
    # #frame will get the last picture from the camera
    ret, frame=cam.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # b = cv2.split(frame)[0]
    # g = cv2.split(frame)[1]
    # r = cv2.split(frame)[2]

    b, g, r = cv2.split(frame)

    blue = cv2.merge((b, blank, blank))
    green = cv2.merge((blank, g, blank))
    red = cv2.merge((blank, blank, r))

    ##merge = cv2.merge((b,g,r))
    merge = cv2.merge((b,r,g))


    cv2.imshow("blue", blue)
    cv2.moveWindow("blue", 700, 0)

    cv2.imshow("green", green)
    cv2.moveWindow("green", 0, 500)

    cv2.imshow("red", red)
    cv2.moveWindow("red", 700, 500)

    ## print(frame.shape)
    ## prints (480, 640, 3) 480 rows 640 columns and 3 elements red blue green 
    ## Grabbing a frame and then showing the frame
    cv2.imshow('piCam', frame)
    cv2.moveWindow('piCam', 0, 0)

    cv2.imshow('merge', merge)
    cv2.moveWindow('merge', 1350, 0)

    ## checks every ms to see if key is pressed
    if cv2.waitKey(1) ==ord('q'):
        break
## need to release camera otherwise will still run
cam.release()
cv2.destroyAllWindows()