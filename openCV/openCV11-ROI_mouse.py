## getting some errors
import cv2
print(cv2.__version__)

goFlag = 0

def mouse_click(event, x, y, flags, params):
    global x1, y1, x2, y2
    global goFlag 
    if event == cv2.EVENT_LBUTTONDOWN:
        x1 = x
        y1 = y
        goFlag = 0
    if event == cv2.EVENT_LBUTTONUP:
        x2 = x
        y2 = y
        goFlag = 1

cv2.namedWindow('piCam')
cv2.setMouseCallback('piCam', mouse_click)

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

    if goFlag == 1:
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 3)
        roi = frame[y1:y2, x1:x2]
        cv2.imshow('ros', roi)
        cv2.moveWindow('ros', 1400, 0)

    cv2.moveWindow('nanoCam', 0, 0)
    ## checks every ms to see if key is pressed
    if cv2.waitKey(1) ==ord('q'):
        break
## need to release camera otherwise will still run
cam.release()
cv2.destroyAllWindows()