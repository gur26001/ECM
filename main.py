###PLEASE NOTE THAT
    # before running you need to see in the middle of the screen else couldn't detect or work properly
    #camera should be clear and perfectly setup and camera should be infront of face directly not capturing from side face,it will work if your face is in front of you
    #you may need to run 1 2 times,sometimes it gets error but after running 2 times it will work
    #assuming initaily not blinked eye  else couldn't detect
    #with glasses some errors may occur else couldn't detect
    #


import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import math
import faceMesh as FM
import irisdetection as irisd
import blinkDetector
#########################################################################
wCam,hCam= 640,480
cam = cv2.VideoCapture(0)
cam.set(3,wCam)
cam.set(4,hCam)
mpDraw = mp.solutions.drawing_utils


#########################################################################
# iris tracking for movement  + it needs initial state for detection
# blink detection for clicking the mouse    +
# facemesh is need for calculating distance of the face and use it accordingly to predict how much to move    -it needs initial state for detection

#########################################################################

LEFT_EYE = [362,382,381,380,374,373,390,249,263,466,388,387,385,384,398]
RIGHT_EYE = [33,7,163,144,145,153,154,155,133,173,157,158,159,160,161,246]

LEFT_IRIS = [474,475,476,477]
RIGHT_IRIS = [469,470,471,472]

wScr,hScr= pyautogui.size()
centerx = 0
centery = 0
d=0
f = 260
W = 6.3
mouseInitialValues = (int(hScr/2),int(wScr/2))

##############################################################
pyautogui.moveTo(mouseInitialValues[0],mouseInitialValues[1])



def findDistance(p1,p2,img=None): #logic and code from cvZone (i copy pasted due to easy of this project , because initially i have used directly mediapipe's facemesh)
    x1, y1 = p1
    x2, y2 = p2
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    length = math.hypot(x2 - x1, y2 - y1)
    return length,(cx,cy)

    pass
def isInc(prev,curr):
    return (prev<curr)
def isDec(prev,curr):
    return (prev>curr)
def initVals():
    intialValues = [0, 0, 0, 0, 0, 0]
    for i in range(0,2):
        istatus, iimg = cam.read()

        ############for calculation  of initial distance of face
        idetector = FM.FaceDetector(maxFaces=1,refinedDetection=True)
        idetector.Process(iimg)
        ipointLeft = idetector.getLandMarkOf(0,145)  # landmark for left eye
        ipointRight =  idetector.getLandMarkOf(0,374)  # landmark for right eye
        iw,ics = findDistance(ipointLeft,ipointRight)

        iF = 260
        iW = 6.3
        initFaceDist = (iW * iF) / iw

        intialValues[0] = iF
        intialValues[1] = iw
        intialValues[2] = iW
        intialValues[3] = initFaceDist

        ############for calculation  of initial iris coordinates
        iIrisdetector = irisd.IrisDetector()
        iIRISES = iIrisdetector.Process(iimg)
        intialValues[4] = (iIRISES[0],iIRISES[2]) #coordinates of left iris,left iris radius
        intialValues[5] = (iIRISES[1],iIRISES[3]) # coordinates of right iris,right iris radius


    return intialValues
######################################

detector2= FM.FaceDetector(refinedDetection=True)
initVs = initVals()

initFaceDist= initVs[3]
movedFaceDist=0
f = 260
W = 6.3
# pyautogui.moveTo(int(wScr/2),int(hScr/2))

initLeftIrisPos = initVs[4][0] #origin(x,y)
initRightIrisPos = initVs[5][0]  #origin(x,y)



if (initVs[5] != 0):
    irisdetector = irisd.IrisDetector()
    while True:
        sat,img= cam.read()
        #########getting landmarks
        # img=cv2.flip(img,1)
        imgRGB= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        ih,iw,cg = img.shape #ignoring color channels to get width and height
        detector2.Process(imgRGB)

        pointLeft = detector2.getLandMarkOf(0, 145)  # landmark for left eye
        pointRight = detector2.getLandMarkOf(0, 374)

        w,cs = findDistance(pointLeft,pointRight)

        currFaceDist= (W*f)/w
        # cv2.circle(img,leftIRISB,1, (255, 0, 255),1)

        irises = irisdetector.Process(img)
        currLeftIris = (irises[0],irises[2])  #origin(x,y),radius
        currRightIris = (irises[1],irises[3]) #origin(x,y),radius


        #right => x inc
        # if(initLeftIrisPos[0]<currLeftIris[0][0]):
        # cv2.putText(img, f'iLeft :{initLeftIrisPos[0], initLeftIrisPos[1]}', (100, 20), cv2.FONT_HERSHEY_PLAIN, 2,(0,255, 0))
        # cv2.putText(img, f'iRight :{initRightIrisPos[0], initRightIrisPos[1]}', (100, 50), cv2.FONT_HERSHEY_PLAIN, 2,(0,255,0))

        initLeftX, initLeftY = np.interp(initLeftIrisPos[0], (0, wCam), (0, wScr)), np.interp(initLeftIrisPos[1],(0, hCam), (0, hScr))
        initRightX, initRightY = np.interp(initRightIrisPos[0], (0, wCam), (0, wScr)), np.interp(initRightIrisPos[1],(0, hCam), (0, hScr))
        cv2.putText(img, f'iLeft :{initLeftX, initLeftY}', (100, 20), cv2.FONT_HERSHEY_PLAIN, 2,(0,255, 0))
        cv2.putText(img, f'iRight :{initRightX, initRightY}', (100, 50), cv2.FONT_HERSHEY_PLAIN, 2,(0,255,0))

        # cv2.putText(img,f'Left :{currLeftIris[0][0],currLeftIris[0][1]}',(100,100),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255))
        # cv2.putText(img, f'Right :{currRightIris[0][0], currRightIris[0][1]}', (100, 200), cv2.FONT_HERSHEY_PLAIN, 2,(255, 0, 255))

        currLeftX,currLeftY =  np.interp(currLeftIris[0][0],(0,wCam),(0,wScr)), np.interp(currLeftIris[0][1],(0,hCam),(0,hScr))
        currRightX, currRightY = np.interp(currRightIris[0][0], (0, wCam), (0, wScr)), np.interp(currRightIris[0][1],(0, hCam), (0, hScr))
        cv2.putText(img,f'Left :{currLeftX,currLeftY}',(100,100),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255))
        cv2.putText(img, f'Right :{currRightX, currRightY}', (100, 200), cv2.FONT_HERSHEY_PLAIN, 2,(255, 0, 255))

        #if left,then calculate according to left|right             DIST=RIGHT,DETECT=LEFT          x dec       write opp because it shows fliped image
        if(int(initLeftX)<int(currLeftX)):
            print("LEFT")
            cv2.putText(img, "LEFT", (100, hScr-100), cv2.FONT_HERSHEY_PLAIN, 2,(0, 255,0))
        # else:
        #     pass
        # if right,then calculate according to left|right            DIST=LEFT,DETECT=RIGHT         x inc     write opp because it shows fliped image
        # if(initLeftIrisPos[0]<currLeftIris[0][0]):
        elif(int(initLeftX)>int(currLeftX)):
            print("RIGHT")
            cv2.putText(img, "RIGHT", (100, hScr - 200), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0))
        else:
            print("")

        # if up,then calculate according to left or right
        if(initRightY>currRightY):
            print("UP")
        elif(initRightY<currRightY):
            print("DOWN")
        else:
            print("")

        # if down,then calculate according to left or right

        # else:
        #     pass
        #########


        cv2.imshow("img",img)
        # cv2.imshow("fliped",fliped)

        if(cv2.waitKey(1)==ord('q')):
            break