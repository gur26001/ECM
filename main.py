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
import keyboard
import math
import faceMesh
import irisdetection as irisd
import distanceDetector
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
mouseInitialValues = (int(hScr/2),int(wScr/2))

##############################################################
pyautogui.moveTo(mouseInitialValues[0],mouseInitialValues[1])


def findDistance(self, p1, p2,img=None):  # logic and code from cvZone (i copy pasted due to easy of this project , because initially i have used directly mediapipe's facemesh)
    x1, y1 = p1
    x2, y2 = p2
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    length = math.hypot(x2 - x1, y2 - y1)
    return length, (cx, cy)


def initVals():
    intialValues = [0, 0, 0, 0]
    idistancedetector = distanceDetector.DistanceDetector()
    iIrisdetector = irisd.IrisDetector()
    for i in range(0,2):
        istatus, iimg = cam.read()
        iIRISES = iIrisdetector.Process(iimg)

        ###iris
        intialValues[2] = (iIRISES[0], iIRISES[2])  # coordinates of left iris,left iris radius
        intialValues[3] = (iIRISES[1], iIRISES[3])  # coordinates of right iris,right iris radius

        ###dist
        iEyesDis,midpoint = idistancedetector.Process(iimg)
        intialValues[0] = iEyesDis  #initial distance of face
        intialValues[1] = midpoint  #initial coordinates of the face distance

        ############for calculation  of initial iris coordinates




    return intialValues
######################################
initVs = initVals()
initLeftIrisPos = initVs[2][0] #origin(x,y)
initRightIrisPos = initVs[3][0]  #origin(x,y)

initFaceDist = initVs[0]
initMidpointCr =  initVs[1]
movedFaceDist=0

# pyautogui.moveTo(int(wScr/2),int(hScr/2))


irisdetector = irisd.IrisDetector()


distancedetector = distanceDetector.DistanceDetector()
while True:
    sat,img= cam.read()
    ih, iw, cg = img.shape  # ignoring color channels to get width and height
    #########getting landmarks

    irises = irisdetector.Process(img)

    currLeftIris = (irises[0],irises[2])  #origin(x,y),radius
    currRightIris = (irises[1],irises[3]) #origin(x,y),radius


    currEyesDis,currMidpointCr = distancedetector.Process(img)


    #right => x inc
    # if(initLeftIrisPos[0]<currLeftIris[0][0]):
    # cv2.putText(img, f'iLeft :{initLeftIrisPos[0], initLeftIrisPos[1]}', (100, 20), cv2.FONT_HERSHEY_PLAIN, 2,(0,255, 0))
    # cv2.putText(img, f'iRight :{initRightIrisPos[0], initRightIrisPos[1]}', (100, 50), cv2.FONT_HERSHEY_PLAIN, 2,(0,255,0))

    initMidX, initMidY = np.interp(initMidpointCr[0], (0, wCam), (0, wScr)), np.interp(initLeftIrisPos[1],(0, hCam), (0, hScr))

    initLeftX, initLeftY = np.interp(initLeftIrisPos[0], (0, wCam), (0, wScr)), np.interp(initLeftIrisPos[1], (0, hCam),(0, hScr))
    initRightX, initRightY = np.interp(initRightIrisPos[0], (0, wCam), (0, wScr)), np.interp(initRightIrisPos[1],(0, hCam), (0, hScr))
    # cv2.putText(img, f'iLeft :{initMidX, initMidY}', (100, 20), cv2.FONT_HERSHEY_PLAIN, 2,(0,255, 0))
    # cv2.putText(img, f'iRight :{initRightX, initRightY}', (100, 50), cv2.FONT_HERSHEY_PLAIN, 2,(0,255,0))

    # cv2.putText(img,f'Left :{currLeftIris[0][0],currLeftIris[0][1]}',(100,100),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255))
    # cv2.putText(img, f'Right :{currRightIris[0][0], currRightIris[0][1]}', (100, 200), cv2.FONT_HERSHEY_PLAIN, 2,(255, 0, 255))

    currMidX,currMidY =  np.interp(currMidpointCr[0],(0,wCam),(0,wScr)), np.interp(currLeftIris[0][1],(0,hCam),(0,hScr))

    currLeftX, currLeftY =  np.interp(currLeftIris[0][0], (0, wCam), (0, wScr)), np.interp(currLeftIris[0][1] ,(0, hCam),(0, hScr))
    currRightX, currRightY = np.interp(currRightIris[0][0], (0, wCam), (0, wScr)),np.interp(currRightIris[0][1], (0, wCam), (0, wScr))
    # cv2.putText(img,f'Left :{currMidX,currMidY}',(100,100),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255))
    # cv2.putText(img, f'Right :{currRightX, currRightY}', (100, 200), cv2.FONT_HERSHEY_PLAIN, 2,(255, 0, 255))


    #to do later irisMidpointY = (currMidY+currRightY)//2

   #if left,then calculate according to left|right             DIST=LEFT,DETECT=LEFT          x dec       write opp because it shows fliped image
    if((initLeftX)<(currLeftX)):
        # movedFaceDist = findDistance((currLeftX,currLeftY),(initLeftX,initLeftY))
        print("LEFT")

    # if right,then calculate according to left|right            DIST=RIGHT,DETECT=RIGHT         x inc     write opp because it shows fliped image

    elif((initRightX)>(currRightX)):
        # movedFaceDist = findDistance(currLeftIris[0], initLeftIrisPos)
        print("RIGHT")

    else:
        print("")

    # if up,then calculate according to left or right

    if(initMidY>currMidY):
        print("UP")
    elif(initMidY<currMidY):
        print("DOWN")
    else:
        print("")

    #########


    cv2.imshow("img",img)
    # cv2.imshow("fliped",fliped) #to do later flip image

    if(keyboard.is_pressed('q')):  #exit
        break
    if(keyboard.is_pressed('s')):  #stop
        cv2.waitKey(0)
    elif(keyboard.is_pressed('r')): #run
        cv2.waitKey(1)

    cv2.waitKey(1)