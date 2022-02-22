import math
import cv2
import commonfile as cf
import faceMesh as FM
import blinkDetector as bd
import irisdetection as irisd
import distanceDetector
import initialState


cam = cv2.VideoCapture(0)
cam.set(3,1280)
cam.set(4,890)

LEFT_IRIS = [474,475,476,477]
RIGHT_IRIS = [469,470,471,472]
MID_NOSE  = [163,6,173,398]
detector = FM.FaceDetector(refinedDetection=True)
distDetector = distanceDetector.DistanceDetector()
irisdetector = irisd.IrisDetector()  #coordinates(left,right) , radius(left,right)
eyestobackheaddistance = 17.53 #avg approx. cm






def moveLeft():
    pass
def moveRight():
    pass
def moveUp():
    pass
def moveDown():
    pass

initVals= initialState.initialstate(cam,detector,distDetector,irisdetector)

initFaceDist = initVals["FaceDist"]  #it is the distance between face and camera taken from the midpoint of eyes width which is almost fixed



while True:
    st,img = cam.read()

    detector.Process(img)


########################################################################################


    leftIrisCorner = detector.getLandMarkOf(0,474) #jisto use krke dist find krna
    leftEyeCorner = detector.getLandMarkOf(0,263)
    leftEyeDis,_ = cf.findDistance(leftIrisCorner,leftEyeCorner)
    # print(leftEyeDis,end=' ')

    rightIrisCorner = detector.getLandMarkOf(0,471)
    rightEyeCorner = detector.getLandMarkOf(0,33)
    rightEyeDis,_ = cf.findDistance(rightEyeCorner,rightIrisCorner)
    # print(rightEyeDis)

    #########right eye's eye shadow detection and its height variation calculated/detected

    leftEyeShadowUpper = detector.getLandMarkOf(0, 257)
    leftEyeShadowDown = detector.getLandMarkOf(0, 386)
    leftEyeShadowDistBtw,_ = cf.findDistance(leftEyeShadowUpper,leftEyeShadowDown)



#########right eye's eye shadow detection and its height variation calculated/detected
    rightEyeShadowUpper = detector.getLandMarkOf(0, 27)
    rightEyeShadowDown = detector.getLandMarkOf(0, 159)
    rightEyeShadowDistBtw,_ = cf.findDistance(leftEyeShadowUpper,leftEyeShadowDown)

    resiris = irisdetector.Process(img)


    cv2.circle(img,resiris[0],2,(0,0,255),-1)
    cv2.circle(img, resiris[1], 2, (0, 0, 255), -1)

    _,eyeshadowdown = cf.findDistance(leftEyeShadowDown,rightEyeShadowDown)


###############eyes movement detection
    if(initVals["EyeDistances"][0]>leftEyeDis): #left
        cv2.putText(img,f'LEFT{initVals["EyeDistances"][0]-leftEyeDis}',(100,100),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255))
    else:
        pass
    if(initVals["EyeDistances"][1]>rightEyeDis): #right
        cv2.putText(img,f'RIGHT{initVals["EyeDistances"][1]-rightEyeDis}',(100,200),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255))
    else:
        pass
    # up
    if(initVals["EyeShadowsDistBtw"][0]>leftEyeShadowDistBtw and initVals["EyeShadowsDistBtw"][1]>rightEyeShadowDistBtw):            #one issue if person is shocked then it will detect as up
        cv2.putText(img, "UP", (100, 150), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255))


    else:
        pass

    #down
    if(initVals["EyeShadowsDistBtw"][0]<leftEyeShadowDistBtw and initVals["EyeShadowsDistBtw"][1]<rightEyeShadowDistBtw):
        cv2.putText(img, "DOWN", (100, 250), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255))
    else:
        pass
########################################
    #<face distance>
    currFaceDist,nosemidpointCr = distDetector.Process(img)
    currFaceDist = int(currFaceDist) #cm
    cv2.putText(img, f'FACE Distance -> {currFaceDist}CM', (500, 250), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
    # cv2.line(img,detector.getLandMarkOf(0,33),detector.getLandMarkOf(0,263),(0,255,0))
     # cv2.line(img,ps[0],ps[1],(0,255,0))
     #
    #</face distance>#

#####distance from nosemidpoint(reference point) to iris of both eyes individually
    movedDist, _ = cf.findDistance(nosemidpointCr, eyeshadowdown)
    cv2.line(img, resiris[1], nosemidpointCr, (0, 255, 0))
    cv2.line(img, resiris[0], nosemidpointCr, (0, 255, 0))

    # left eye angle from reference line
    leftirisdisfromnosemid, _ = cf.findDistance(resiris[0],nosemidpointCr)
    # cv2.circle(img, _, 2, (255, 0, 0), -1)
    ltantheta = (leftirisdisfromnosemid / eyestobackheaddistance)
    estimatedLDist = int(ltantheta*(eyestobackheaddistance+currFaceDist)) #cm

    print("LEFT ESTIMATED",ltantheta," ",estimatedLDist)

    # right eye angle from reference line
    rightirisdisfromnosemid, _ = cf.findDistance(resiris[1],nosemidpointCr)
    # cv2.circle(img,_,2,(255,0,0),-1)
    rtantheta = (rightirisdisfromnosemid / eyestobackheaddistance)
    estimatedRDist = int(rtantheta * (eyestobackheaddistance + currFaceDist))

    print("RIGHT ESTIMATED",rtantheta," ",estimatedRDist)

    irisesMidpoint,irisesMidpointCrs = cf.findDistance(resiris[0],resiris[1])
    #for eyes up00
    irismidupdistance,_ = cf.findDistance(irisesMidpointCrs,nosemidpointCr) #postitive
    utantheta = irismidupdistance/eyestobackheaddistance

    estimatedUDist = int(utantheta*(eyestobackheaddistance+currFaceDist))
    print("UP ESTIMATED  ",utantheta," ",estimatedUDist)
    # for eyes down  #negative
############################################





































    cv2.imshow("img",img)
    if(cv2.waitKey(1)==ord('q')):
        break
