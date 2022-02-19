import cv2
import commonfile as cf
import faceMesh as FM
import blinkDetector as bd
import irisdetection as irisd

cam = cv2.VideoCapture(0)
cam.set(3,1280)
cam.set(4,890)
LEFT_IRIS = [474,475,476,477]
RIGHT_IRIS = [469,470,471,472]
MID_NOSE  = [163,6,173,398]
detector = FM.FaceDetector(refinedDetection=True)


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


        val=[(leftEyeDis,rightEyeDis),(leftEyeShadowDistBtw,rightEyeShadowDistBtw)]

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


while True:
    st,img = cam.read()


    #left -> distance b/w eye corner point in direction of the eye outside corner

    detector.Process(img)
    # for i in LEFT_IRIS:
    #     lefteye = detector.getLandMarkOf(0,i)
    #     cv2.putText(img,f'{i}',lefteye,cv2.FONT_HERSHEY_PLAIN,0.5,(0,255,0))
    # for i in RIGHT_IRIS:
    #     righteye = detector.getLandMarkOf(0, i)
    #     cv2.putText(img, f'{i}', righteye, cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 255, 0))
    #
    # righteye = detector.getLandMarkOf(0,33)
    # cv2.putText(img, f'{33}', righteye, cv2.FONT_HERSHEY_PLAIN, 0.5, (255, 255, 0))
    # right -> distance b/w eye corner point in direction of the eye outside corner


##################For detection of the mid of the nose to get the reference line for left and right angle
    centerofnose= detector.getLandMarkOf(0,168)
    cv2.circle(img,centerofnose,2,(0,0,255),-1)
########################################################################################
###################For detection of the up and down


########################################################################################


    leftIrisCorner = detector.getLandMarkOf(0,474 ) #jisto use krke dist find krna
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
    cv2.putText(img,f'{eyeshadowdown}',(eyeshadowdown[0]-10,eyeshadowdown[1]-10),cv2.FONT_HERSHEY_PLAIN,1,(0,255,255))
    cv2.circle(img,eyeshadowdown,5,(255,0,255),-1)

    # rightIrisDis = format((cf.findDistance(resiris[1],valright)[0]),".2f")
    # cv2.putText(img,f'dist{rightIrisDis}',(resiris[1][0]-10,resiris[1][1]-5),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),1)
    #
    #
    cv2.line(img,resiris[1],centerofnose,(0,255,0))
    #
    #
    # leftIrisDis = format((cf.findDistance(resiris[0],valleft)[0]),".2f")
    # cv2.putText(img,f'dist{leftIrisDis}',(resiris[0][0] - 10, resiris[0][1] - 5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
    #
    cv2.line(img,resiris[0],centerofnose,(0,255,0))

    # cv2.putText(img, f'dist{cf.findDistance(detector.getLandMarkOf(0, 469), detector.getLandMarkOf(0, 133))[0]}',(resiris[1][0] - 10, resiris[1][1] - 10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    # cv2.line(img, detector.getLandMarkOf(0, 469), detector.getLandMarkOf(0, 133), (0, 255, 0))

    if(initVals[0][0]>leftEyeDis): #left
        cv2.putText(img,f"LEFT{initVals[0][0]-leftEyeDis}",(100,100),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255))

    else:
        pass
    if(initVals[0][1]>rightEyeDis): #right
        cv2.putText(img,f"RIGHT{initVals[0][1]-rightEyeDis}",(100,200),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255))
    else:
        pass
    if(initVals[1][0]>leftEyeShadowDistBtw and initVals[1][1]>rightEyeShadowDistBtw):#up            one issue if person is shocked then it will detect as up
        cv2.putText(img, "UP", (100, 150), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255))
    else:
        pass

    #down ka issue ki vo kahi blink na krde vali situation
    if(initVals[1][0]<leftEyeShadowDistBtw and initVals[1][1]<rightEyeShadowDistBtw):
        cv2.putText(img, "DOWN", (100, 250), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255))
    else:
        pass
    cv2.imshow("img",img)
    if(cv2.waitKey(1)==ord('q')):
        break
