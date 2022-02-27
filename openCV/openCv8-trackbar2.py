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

## need to create a trackbar in window so need to create 
cv2.namedWindow('piCam')

def nothing():
    pass

## requires callback function, this case were giving nothing as don't need anything
cv2.createTrackbar('xVal', 'piCam', 25, dispW, nothing)
cv2.createTrackbar('yVal', 'piCam', 25, dispH, nothing)

cv2.createTrackbar('width', 'piCam', 25, dispH, nothing)
cv2.createTrackbar('height', 'piCam', 25, dispH, nothing)

while True:
    ## ret allows creating the var
    ##frame will get the last picture from the camera
    ret, frame=cam.read()

    xVal = cv2.getTrackbarPos('xVal', 'piCam')
    yVal = cv2.getTrackbarPos('yVal', 'piCam')

    height = cv2.getTrackbarPos('height', 'piCam')
    width = cv2.getTrackbarPos('width', 'piCam')

    cv2.circle(frame, (xVal, yVal), 5, (255,0,0), -1)
    cv2.rectangle(frame, (xVal, yVal), (xVal + width, yVal + height), (255,0,0), 3)

    ## Grabbing a frame and then showing the frame
    cv2.imshow('piCam', frame)
    cv2.moveWindow('piCam', 0, 0)
    ## checks every ms to see if key is pressed
    if cv2.waitKey(1) ==ord('q'):
        break
## need to release camera otherwise will still run
cam.release()
cv2.destroyAllWindows()