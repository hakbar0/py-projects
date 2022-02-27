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

## get dispW direct from rasp pi camera
dispW = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
dispH = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

## box width 
BW = int(.25*dispW)
BH = int(.25*dispH)
posX = 10
posY = 270
dx = 2
dy = 2

while True:
    ## ret allows creating the var
    # #frame will get the last picture from the camera
    ret, frame=cam.read()

    cv2.moveWindow('piCam', 0, 0)
    frame = cv2.rectangle(frame,(posX, posY), (posX+BW,posY+BH), (255,0,0),-1)

    ## Grabbing a frame and then showing the frame
    cv2.imshow('piCam', frame)

    posX += dx
    posY += dy

    if posX <= 0 or posX + BW >= dispW:
        dx *= -1
    
    if posY <= 0 or posY + BH >= dispH:
        dy *= -1

    ## checks every ms to see if key is presse
    if cv2.waitKey(1) ==ord('q'):
        break
## need to release camera otherwise will still run
cam.release()
cv2.destroyAllWindows()