import cv2
print(cv2.__version__)

### a picture is a matrix
## wdith is columns
## height is rows
## so when we go to the column and row we find a tuple with a colour.

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

    ## region of interst
    ## matrix is row,col so y,x
    ## if roi is equal to frame and not a copy it is ref it.
    ## so if frame changes so wil roi
    roi = frame[50:250, 200:400].copy()
    roiGray = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)

    ## change some of the frame, to completely white
    frame[50:250, 200:400] = [255, 255, 255]

    cv2.imshow('ROI', roi)
    cv2.imshow('GRAY', roiGray)

    ## Grabbing a frame and then showing the frame
    cv2.imshow('piCam', frame)

    cv2.moveWindow('piCam', 0, 0)
    cv2.moveWindow('ROI', 1300, 0)
    cv2.moveWindow('GRAY', 1300, 250)

    ## checks every ms to see if key is pressed
    if cv2.waitKey(1) ==ord('q'):
        break
## need to release camera otherwise will still run
cam.release()
cv2.destroyAllWindows()