import cv2
print(cv2.__version__)

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
    cv2.imshow('piCam', frame)
    cv2.moveWindow('piCam', 700, 0)

    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    frameSmall = cv2.resize(frame, (320,240))
    graySmall = cv2.resize(gray, (320,240))

    cv2.moveWindow('BW', 0, 265)
    cv2.moveWindow('nanoSmall', 0, 0)

    cv2.imshow('BW', graySmall)
    cv2.imshow('nanoSmall', frameSmall)

    cv2.moveWindow('BW2', 385, 265)
    cv2.moveWindow('nanoSmall2', 385, 0)

    cv2.imshow('BW2', graySmall)
    cv2.imshow('nanoSmall2', frameSmall)

    ## checks every ms to see if key is pressed
    if cv2.waitKey(1) ==ord('q'):
        break
## need to release camera otherwise will still run
cam.release()
cv2.destroyAllWindows()