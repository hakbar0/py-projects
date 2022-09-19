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

## import the face cascade model
face_cascade=cv2.CascadeClassifier('/home/nvidia/Desktop/py-projects/cascade/face.xml')

while True:
    # #frame will get the last picture from the camera
    ret, frame=cam.read()

    ##convert to grey as less computatial power
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    ##See If i can find a face, returns an array of a box corners
    ##1.3,5 is setting tolerance
    ## faces will be a list of arrays
    faces=face_cascade.detectMultiScale(gray)
    ## draw rectangles on face
    ## set colour and line width
    for(x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2)

    cv2.imshow('piCam', frame)
    cv2.moveWindow('piCam', 0, 0)

    ## checks every ms to see if key is pressed
    if cv2.waitKey(1) ==ord('q'):
        break
## need to release camera otherwise will still run
cam.release()
cv2.destroyAllWindows()