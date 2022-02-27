import cv2
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

while True:
    ## ret allows creating the var
    # #frame will get the last picture from the camera
    ret, frame=cam.read()
    ## Grabbing a frame and then showing the frame
    cv2.imshow('piCam', frame)
    ## postions camera at top left corner
    cv2.moveWindow('piCam', 0, 0)
    ## checks every ms to see if key is pressed

    cv2.imshow('piCam2', frame)
    cv2.moveWindow('piCam2', 700, 0)

    ## Set new frame in grayscale format
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('greyVideo', grey)
    cv2.moveWindow('greyVideo', 0, 520)

    cv2.imshow('greyVideo2', grey)
    cv2.moveWindow('greyVideo2', 700, 520)

    if cv2.waitKey(1) ==ord('q'):
        break
## need to release camera otherwise will still run
cam.release()
cv2.destroyAllWindows()