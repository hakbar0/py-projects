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
    ## frame will get the last picture from the camera
    ret, frame=cam.read()
    ## setting  blue box
    frame = cv2.rectangle(frame, (140,100), (250,170), (255,0,0),4)
    ## setting green box
    frame = cv2.rectangle(frame, (150,100), (180,140), (0,255,0),4)
    ## Setting red circle, to make solid make width to -1
    frame = cv2.circle(frame, (350,350), 50, (0,0,255),-1)
    # creating font
    fnt = cv2.FONT_HERSHEY_DUPLEX
    frame=cv2.putText(frame, 'My First Text', (300, 300), fnt, 1.5, (255,0,150), 2)
    frame=cv2.line(frame, (10,10), (630, 470), (0,0,0), 4)
    frame=cv2.arrowedLine(frame, (10,470),(630,10), (255,255,255), 3)
    ## Grabbing a frame and then showing the frame
    cv2.imshow('piCam', frame)
    ## checks every ms to see if key is pressed
    cv2.moveWindow('piCam', 0, 0)
    if cv2.waitKey(1) ==ord('q'):
        break
## need to release camera otherwise will still run
cam.release()
cv2.destroyAllWindows()