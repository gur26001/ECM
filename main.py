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
    intialValues = [0, 0, 0, 0, 0, 0, 0 , 0 ,0]
    for i in range(0,2):
        istatus, iimg = cam.read()
        detector = FM.FaceDetector(maxFaces=1,refinedDetection=True)
        detector.Process(iimg)
        ipointLeft = detector.getLandMarkOf(0,145)  # landmark for left eye
        ipointRight =  detector.getLandMarkOf(0,374)  # landmark for right eye
        ileftIRISB = detector.getLandMarkOf(0, LEFT_IRIS[3])

        iw,ics = findDistance(ipointLeft,ipointRight)
        icenterx= ics[0]
        icentery= ics[1]

        iF = 260
        iW = 6.3
        initFaceDist = (iW * iF) / iw

        intialValues[0] = iF
        intialValues[1] = iw
        intialValues[2] = iW
        intialValues[3] = initFaceDist
        intialValues[4] = ipointLeft
        intialValues[5] = ipointRight
        intialValues[6] = icenterx
        intialValues[7] = icentery
        intialValues[8] = ileftIRISB

    return intialValues
######################################
# with myFaceMesh.FaceMesh(max_num_faces=1,refine_landmarks=True,min_detection_confidence=0.5,min_tracking_confidence=0.5) as facemesh :

detector2= FM.FaceDetector(refinedDetection=True)

initVs = initVals()

initLEFTIRISx=initVs[8][0]
initLEFTIRISy=initVs[8][1]
initFaceDist= initVs[3]
movedFaceDist=0
f = 260
W = 6.3
pyautogui.moveTo(int(wScr/2),int(hScr/2))
if (initVs[5] != 0):
    while True:
        sat,img= cam.read()
        #########getting landmarks
        img=cv2.flip(img,1)
        imgRGB= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        ih,iw,cg = img.shape #ignoring color channels to get width and height
        detector2.Process(imgRGB)
        leftIRISB = detector2.getLandMarkOf(0,LEFT_IRIS[3])

        pointLeft = detector2.getLandMarkOf(0, 145)  # landmark for left eye
        pointRight = detector2.getLandMarkOf(0, 374)
        w,cs = findDistance(pointLeft,pointRight)

        currFaceDist= (W*f)/w
        # cv2.circle(img,leftIRISB,1, (255, 0, 255),1)
        currLEFTIRISx = leftIRISB[0]
        currLEFTIRISy = leftIRISB[1]


        if(isInc(initLEFTIRISx,currLEFTIRISx)):     #majorly x(horizontal coordinate)  is inc
            movedFaceDist = currLEFTIRISx-initLEFTIRISx
            cv2.putText(img, f'RIGHT, MOVED=>{movedFaceDist}', (50, 79), cv2.FONT_HERSHEY_PLAIN,2, (255, 0, 255))

            theta1 = math.atan(movedFaceDist / initFaceDist)  # inverse of tan => atan in python in radians
            #
            estiFaceRemDis = math.tan(theta1 + 0.0349066) * currFaceDist
            #
            totald = movedFaceDist + estiFaceRemDis
            if(pyautogui.position()[0]<wScr):
                try:
                    pyautogui.moveTo(pyautogui.position()[0]+totald, pyautogui.position()[1])
                except:
                    try:
                        if pyautogui.position()[1] > hScr:
                            pyautogui.moveTo(x=wScr,y=hScr-1)
                        elif pyautogui.position()[1]<0:
                            pyautogui.moveTo(x=wScr, y=1)
                        else:
                            pyautogui.moveTo(x=wScr,y=pyautogui.position()[1])
                    except:
                        print("move in the region")


        # left

        elif(isDec(initLEFTIRISx,currLEFTIRISx)):                   #majorly x(vertical coordinate)  is dec
            movedFaceDist = currLEFTIRISx - initLEFTIRISx
            cv2.putText(img,  f'LEFT, MOVED=>{movedFaceDist}', (51, 81), cv2.FONT_HERSHEY_PLAIN,2, (255, 0, 255))

            theta1 = math.atan(movedFaceDist / initFaceDist)  # inverse of tan => atan in python in radians
            #
            estiFaceRemDis = math.tan(theta1 + 0.0349066) * currFaceDist
            #
            totald=movedFaceDist+estiFaceRemDis
            #
            if (pyautogui.position()[0] >0):
                try:
                    pyautogui.moveTo(totald-pyautogui.position()[0], pyautogui.position()[1])
                except:
                    try:
                        if pyautogui.position()[1] > hScr:
                            pyautogui.moveTo(x=0,y=hScr-1)
                        elif pyautogui.position()[1]<0:
                            pyautogui.moveTo(x=0, y=1)
                        else:
                            pyautogui.moveTo(x=0,y=pyautogui.position()[1])
                    except:
                        print("move in the region")

    #
        else:
            pass
        # down
        if(isInc(initLEFTIRISy,currLEFTIRISy)):      #majorly y(vertical coordinate)  is inc
            movedFaceDist = currLEFTIRISy - initLEFTIRISy
            cv2.putText(img,  f'DOWN, MOVED=>{movedFaceDist}', (53, 203), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255))

            theta1 = math.atan(movedFaceDist / initFaceDist)  # inverse of tan => atan in python in radians
            #
            estiFaceRemDis = math.tan(theta1 + 0.0349066) * currFaceDist
            totald = movedFaceDist + estiFaceRemDis
            if (pyautogui.position()[1] < hScr):
                try:
                    pyautogui.moveTo(pyautogui.position()[0],totald+pyautogui.position()[1])
                except:
                    try:
                        if pyautogui.position()[0] > wScr:
                            pyautogui.moveTo(x=wScr-1, y=hScr)
                        elif pyautogui.position()[0] < 0:
                            pyautogui.moveTo(x=1, y=hScr)
                        else:
                            pyautogui.moveTo(x=pyautogui.position()[0], y=hScr)
                    except:
                        print("move in the region")

        # up
        # else:
        #     pass
        elif(isDec(initLEFTIRISy,currLEFTIRISy)):                      #majorly y(vertical coordinate)  is dec
            movedFaceDist = currLEFTIRISy - initLEFTIRISy
            cv2.putText(img, f'UP, MOVED=>{movedFaceDist}', (52, 102), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255))

            theta1 = math.atan(movedFaceDist / initFaceDist)  # inverse of tan => atan in python in radians
            #
            estiFaceRemDis = math.tan(theta1 + 0.0349066) * currFaceDist
            totald = movedFaceDist + estiFaceRemDis
            if (pyautogui.position()[1] >   0):
                try:
                    pyautogui.moveTo(pyautogui.position()[0], totald-pyautogui.position()[1])
                except:
                    try:
                        if pyautogui.position()[0] > wScr:
                            pyautogui.moveTo(x=wScr-1, y=0)
                        elif pyautogui.position()[0] < 0:
                            pyautogui.moveTo(x=1, y=0)
                        else:
                            pyautogui.moveTo(x=pyautogui.position()[0], y=0)
                    except:
                        print("move in the region")

        else:
            pass


        # irisx=leftIRISB[0]    #assumed both eyes are right(move simultaneously except eye disease of unbalanced eye movement)=>we are getting coordinates of one of the eye
        # irisy=leftIRISB[1]
        #
        # tx= np.interp(irisx,(0,wCam),(0,wScr))
        # ty= np.interp(irisy,(0,hCam),(0,hScr))
        #
        # pyautogui.moveTo(tx+100, ty+100)

        #########
        cv2.imshow("img",img)
        # cv2.imshow("fliped",fliped)

        if(cv2.waitKey(1)==ord('q')):
            break