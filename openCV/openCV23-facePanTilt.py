import cv2
print(cv2.__version__)

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
    # #frame will get the last picture from the camera
    ret, frame=cam.read()

    cv2.imshow('piCam', frame)
    cv2.moveWindow('piCam', 0, 0)

    ## checks every ms to see if key is pressed
    if cv2.waitKey(1) ==ord('q'):
        break
## need to release camera otherwise will still run
cam.release()
cv2.destroyAllWindows()