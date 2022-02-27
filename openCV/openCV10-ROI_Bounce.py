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

BW = int(0.2*dispW)
BH = int(0.2*dispW)

posX = 10
posY = 270
dx = 2
dy = 2

while True:
    ## ret allows creating the var
    # #frame will get the last picture from the camera
    ret, frame=cam.read()

    roi = frame[posY:posY+BH, posX:posX+BW].copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ## need to convert back get color to get gray
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    ## square will be colour
    frame[posY:posY+BH, posX:posX+BW] = roi
    cv2.rectangle(frame, (posX, posY), (posX+BW, posY+BH), (255, 0, 0), 3)

    ## Grabbing a frame and then showing the frame
    cv2.imshow('piCam', frame)
    cv2.moveWindow('piCam', 0, 0)

    posX += dx
    posY += dy

    if posX + BW >= dispW or posX <= 0:
        dx *= -1

    if posY + BH >= dispH or posY <= 0:
        dy *= -1

    ## checks every ms to see if key is pressed
    if cv2.waitKey(1) ==ord('q'):
        break
## need to release camera otherwise will still run
cam.release()
cv2.destroyAllWindows()