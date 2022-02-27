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

## read logo
PL = cv2.imread('pl.jpg')
PL = cv2.resize(PL, (75, 75))
cv2.imshow('LogoWindow', PL)
cv2.moveWindow('LogoWindow', 700, 0)

## Convert to grayscale
PLGray = cv2.cvtColor(PL, cv2.COLOR_BGR2GRAY)
cv2.imshow('LGGray', PLGray)
cv2.moveWindow('LGGray', 800, 0)

## creating background mask
## if that bixel is greater than 245 i want it to be white
_,BGMask = cv2.threshold(PLGray, 245,255, cv2.THRESH_BINARY)
cv2.imshow('BGMask', BGMask)
cv2.moveWindow('BGMask', 900, 0)

## foreground mask
FGMask = cv2.bitwise_not(BGMask)
cv2.imshow('FGMask', FGMask)
cv2.moveWindow('FGMask', 1000, 0)

## Foreground
FG = cv2.bitwise_and(PL, PL, mask=FGMask)
cv2.imshow('FG', FG)
cv2.moveWindow('FG', 1100, 0)

## Box
BW = 75
BH = 75
Xpos = 10
ypos = 10
dx = 1
dy = 1

while True:
    ## ret allows creating the var
    # #frame will get the last picture from the camera
    ret, frame=cam.read()

    ## Region ofi nterest
    ROI = frame[ypos: ypos+BH, Xpos:Xpos+BW]
    ROIBG = cv2.bitwise_and(ROI, ROI, mask=BGMask)
    cv2.imshow('ROIBG', ROIBG)
    cv2.moveWindow('ROIBG', 1200, 0)

    ## Foreground for ROI as black is 0 so anything added will get the color
    ROInew = cv2.add(FG, ROIBG)
    cv2.imshow('ROInew', ROInew)
    cv2.moveWindow('ROInew', 1300, 0)
    frame[ypos:ypos+BH, Xpos:Xpos+BW] = ROInew

    ##Change pos 
    Xpos = Xpos + dx
    ypos = ypos + dy

    ##
    if Xpos <= 0 or Xpos+BW >= dispW:
        dx *= -1
    if ypos <= 0 or ypos+BH >= dispH:
        dy *= -1
 
    ## Grabbing a frame and then showing the frame
    cv2.imshow('piCam', frame)
    cv2.moveWindow('piCam', 0, 0)
    ## checks every ms to see if key is pressed
    if cv2.waitKey(1) ==ord('q'):
        break
## need to release camera otherwise will still run
cam.release()
cv2.destroyAllWindows()