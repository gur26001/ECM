import math

import cv2
import commonfile as cf
import faceMesh as FM
import blinkDetector as bd
import irisdetection as irisd
import distanceDetector

cam = cv2.VideoCapture(0)
cam.set(3,1280)
cam.set(4,890)
LEFT_IRIS = [474,475,476,477]
RIGHT_IRIS = [469,470,471,472]
MID_NOSE  = [163,6,173,398]
detector = FM.FaceDetector(refinedDetection=True)
distDetector = distanceDetector.DistanceDetector()
# midnoseDistFromBackOfHead = # cm


def initialState():
    val=0
    for i in range(0,5):
        st, img = cam.read()
        detector.Process(img)

        leftIrisCorner = detector.getLandMarkOf(0, 474)  # jisto use krke dist find krna
        leftEyeCorner = detector.getLandMarkOf(0, 263)
        leftEyeDis, _ = cf.findDistance(leftIrisCorner, leftEyeCorner)
        print(leftEyeDis, end=' ')

        rightIrisCorner = detector.getLandMarkOf(0, 471)
        rightEyeCorner = detector.getLandMarkOf(0, 33)
        rightEyeDis, _ = cf.findDistance(rightEyeCorner, rightIrisCorner)
        print(rightEyeDis)

        leftEyeShadowUpper = detector.getLandMarkOf(0, 257)
        leftEyeShadowDown = detector.getLandMarkOf(0, 386)
        leftEyeShadowDistBtw, _ = cf.findDistance(leftEyeShadowUpper, leftEyeShadowDown)


        rightEyeShadowUpper = detector.getLandMarkOf(0, 27)
        rightEyeShadowDown = detector.getLandMarkOf(0, 159)
        rightEyeShadowDistBtw, _ = cf.findDistance(leftEyeShadowUpper, leftEyeShadowDown)

        ##########
        faceDist,_ =distDetector.Process(img)

        val=[(leftEyeDis,rightEyeDis),(leftEyeShadowDistBtw,rightEyeShadowDistBtw),faceDist]

    return val

def moveLeft():
    pass
def moveRight():
    pass
def moveUp():
    pass
def moveDown():
    pass

initVals= initialState()

irisdetector = irisd.IrisDetector()  #coordinates(left,right) , radius(left,right)

# faceMid = [168,6,]
initFaceDist = initVals[2]  #it is the distance between face and camera taken from the midpoint of eyes width which is almost fixed


while True:
    st,img = cam.read()

    detector.Process(img)


##################For detection of the mid of the nose to get the reference line for left and right angle
    centerofnose= detector.getLandMarkOf(0,168)
    cv2.circle(img,centerofnose,2,(0,0,255),-1)
########################################################################################
###################For detection of the up and down


########################################################################################


    leftIrisCorner = detector.getLandMarkOf(0,474) #jisto use krke dist find krna
    leftEyeCorner = detector.getLandMarkOf(0,263)
    leftEyeDis,_ = cf.findDistance(leftIrisCorner,leftEyeCorner)
    # print(leftEyeDis,end=' ')

    rightIrisCorner = detector.getLandMarkOf(0,471)
    rightEyeCorner = detector.getLandMarkOf(0,33)
    rightEyeDis,_ = cf.findDistance(rightEyeCorner,rightIrisCorner)
    # print(rightEyeDis)

    leftEyeShadowUpper = detector.getLandMarkOf(0, 257)
    leftEyeShadowDown = detector.getLandMarkOf(0, 386)


    leftEyeShadowDistBtw,_ = cf.findDistance(leftEyeShadowUpper,leftEyeShadowDown)




    rightEyeShadowUpper = detector.getLandMarkOf(0, 27)
    rightEyeShadowDown = detector.getLandMarkOf(0, 159)
    rightEyeShadowDistBtw,_ = cf.findDistance(leftEyeShadowUpper,leftEyeShadowDown)

    resiris = irisdetector.Process(img)

    cv2.circle(img,resiris[0],2,(0,0,255),-1)
    cv2.circle(img, resiris[1], 2, (0, 0, 255), -1)


    _,eyeshadowdown = cf.findDistance(leftEyeShadowDown,rightEyeShadowDown)

    movedDist,_=cf.findDistance(centerofnose,eyeshadowdown)
    cv2.line(img,centerofnose,eyeshadowdown,(255,255,0),2)

    cv2.line(img,resiris[1],centerofnose,(0,255,0))
    cv2.line(img,resiris[0],centerofnose,(0,255,0))


###############3eyes movement detection
    if(initVals[0][0]>leftEyeDis): #left
        cv2.putText(img,f"LEFT{initVals[0][0]-leftEyeDis}",(100,100),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255))

    else:
        pass
    if(initVals[0][1]>rightEyeDis): #right
        cv2.putText(img,f"RIGHT{initVals[0][1]-rightEyeDis}",(100,200),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255))
    else:
        pass
    # up
    if(initVals[1][0]>leftEyeShadowDistBtw and initVals[1][1]>rightEyeShadowDistBtw):            #one issue if person is shocked then it will detect as up
        cv2.putText(img, "UP", (100, 150), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255))
        # utheta1 = math.atan()

    else:
        pass

    #down
    if(initVals[1][0]<leftEyeShadowDistBtw and initVals[1][1]<rightEyeShadowDistBtw):
        cv2.putText(img, "DOWN", (100, 250), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255))
    else:
        pass
########################################
    #<face distance>
    currFaceDist,ps = distDetector.Process(img)
    currFaceDist = int(currFaceDist)
    cv2.putText(img, f'FACE Distance -> {(currFaceDist)}', (500, 250), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
    cv2.line(img,ps[0],ps[1],(0,255,0))


    #</face distance>#

    cv2.imshow("img",img)
    if(cv2.waitKey(1)==ord('q')):
        break
