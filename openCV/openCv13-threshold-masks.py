import cv2
print(cv2.__version__)

def nothing():
    pass

cv2.namedWindow('Blended')    
cv2.createTrackbar('BlendValue', 'Blended', 50, 100, nothing)

## want to keep this aspect ratio
## display width/height
dispW=320
dispH=240

## Images have to be same size to mask
cvLogo = cv2.imread('cv.jpg')
cvLogo = cv2.resize(cvLogo, (320, 240))

cvLogoGray = cv2.cvtColor(cvLogo, cv2.COLOR_BGR2GRAY)

cv2.imshow('cv Logo Gray', cvLogoGray)
cv2.moveWindow('cv Logo Gray', 0, 350)

## Compare each pixel to threshold value if below make it black or above white
_,BGMask = cv2.threshold(cvLogoGray, 225, 255, cv2.THRESH_BINARY)
cv2.imshow('BG Mask', BGMask)
cv2.moveWindow('BG Mask', 385, 100)

## Build forground mask as opposite of background
FGMask = cv2.bitwise_not(BGMask)
cv2.imshow('FG Mask', FGMask)
cv2.moveWindow('FG Mask', 385, 350)

## combines with original colour
FG = cv2.bitwise_and(cvLogo, cvLogo, mask=FGMask)
cv2.imshow('FG', FG)
cv2.moveWindow('FG', 703, 350)

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

    ## Behind mask for if white we replace it
    BG = cv2.bitwise_and(frame, frame, mask=BGMask)
    cv2.imshow('BG', BG)
    cv2.moveWindow('BG', 703, 100)

    ## if you add black to anything you get anthing
    compImage = cv2.add(BG, FG)
    cv2.imshow('compImage', compImage)
    cv2.moveWindow('compImage', 1017, 100)

    ## To get trackbar pos, divide by 100 to get a value between 0 and 1
   
    BV = cv2.getTrackbarPos('BlendValue', 'Blended')/100
    BV2 = 1 - BV
   
    ## As BV increases BV2 will decerease so the camera has more transprancey
    Blended = cv2.addWeighted(frame, BV, cvLogo, BV2, 0)
    cv2.imshow('Blended', Blended)
    cv2.moveWindow('Blended', 1017, 350)

    FG2 = cv2.bitwise_and(Blended, Blended, mask=FGMask)
    cv2.imshow('FG2', FG2)
    cv2.moveWindow('FG2', 1324, 100)

    compFinal = cv2.add(BG, FG2)
    cv2.imshow('compFinal', compFinal)
    cv2.moveWindow('compFinal', 1324, 350)

    ## Grabbing a frame and then showing the frame
    cv2.imshow('piCam', frame)
    cv2.moveWindow('piCam', 0, 100)
    ## checks every ms to see if key is pressed
    if cv2.waitKey(1) ==ord('q'):
        break
## need to release camera otherwise will still run
cam.release()
cv2.destroyAllWindows()