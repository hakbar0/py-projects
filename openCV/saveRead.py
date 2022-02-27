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
## cam = cv2.VideoCapture(camSet)

## to capture from file
cam = cv2.VideoCapture('videos/myCam.avi')

## don't start with slash as starts with route
## second parameter is video format
## third is frame rate
## four is heigh and width
##  outVid = cv2.VideoWriter('videos/myCam.avi', cv2.VideoWriter_fourcc(*'XVID'), 21, (dispW, dispH)) 

while True:
    ## ret allows creating the var
    # #frame will get the last picture from the camera
    ret, frame=cam.read()
    ## Grabbing a frame and then showing the frame
    cv2.imshow('piCam', frame)
    cv2.moveWindow('piCam', 0, 0)
    ## We write the frame to the video
    ##  outVid.write(frame)
    ## checks every ms to see if key is pressed
    ## Change to 50 if want to delay it
    if cv2.waitKey(50) ==ord('q'):
        break
## need to release camera otherwise will still run
cam.release()
outVid.release()
cv2.destroyAllWindows()