import cv2
import numpy as np
print(cv2.__version__)

evt = -1
## arrays seem global in open cv
coord = []
## Create tuple with 250 rows and 250 columns with 3 postions in it
img = np.zeros((250,250,3), np.uint8)

## need to provide flags and params even though we don't use as setmousecallaback provides that
def click(event, x, y, flags, params):
    global pnt
    global evt

    if event == cv2.EVENT_LBUTTONDOWN:
        print('Mouse event was: ', event)
        print(x, ',', y)
        pnt=(x,y)
        coord.append(pnt)
        print(coord)
        evt=event
    if event == cv2.EVENT_RBUTTONDOWN:
        print(x,y)
        ## frame is a 2d matrix
        ## when dealing with matrice we the y value is the row and the x value is the column
        ## RGB (0 ,0, 0)
        blue = frame[y, x, 0]
        green = frame[y, x, 1]
        red = frame[y, x, 2]
        print(blue,green,red) 
        colorString = str(blue) + ',' + str(green) + ',' + str(red)
        ## colon says take everything and set it to tue color
        img[:]=[blue,green,red]
        fnt = cv2.FONT_HERSHEY_PLAIN
        r = 255 - int(red)
        g = 255 - int(green)
        b = 255 - int(blue)
        tp=(b,g,r)

        cv2.putText(img, colorString, (10,25), fnt, 1, tp, 2)
        cv2.imshow('myColor', img)


## want to keep this aspect ratio
## display width/height
dispW=1280
dispH=960

## if not 4 camera will be upside down, or horizontally flipped 
flip = 4

## Mouse callback, need to set the window before we set the callback
cv2.namedWindow('piCam')
cv2.setMouseCallback('piCam', click)

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

    for pnts in coord:
        cv2.circle(frame, pnts, 5, (0,0,255), -1)
        font = cv2.FONT_HERSHEY_PLAIN
        myStr = str(pnts)
        cv2.putText(frame, myStr, pnts, font, 1.5, (255, 0, 0), 2)

    ## Grabbing a frame and then showing the frame
    cv2.imshow('piCam', frame)
    cv2.moveWindow('piCam', 0, 0)

    keyEvent = cv2.waitKey(1)
    ## checks every ms to see if key is pressed
    if keyEvent == ord('q'):
        break

    if keyEvent == ord('c'):
        coord = []

## need to release camera otherwise will still run
cam.release()
cv2.destroyAllWindows()