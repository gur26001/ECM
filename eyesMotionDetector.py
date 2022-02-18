import cv2
import commonfile as cf
import faceMesh as FM
import blinkDetector as bd

cam = cv2.VideoCapture(0)
cam.set(3,1280)
cam.set(4,890)
LEFT_IRIS = [474,475,476,477]
RIGHT_IRIS = [469,470,471,472]
detector = FM.FaceDetector(refinedDetection=True)

def initialState():
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

        cv2.imshow("img", img)
        if (cv2.waitKey(1) == ord('q')):
            break
    return [(leftEyeDis,rightEyeDis),(leftEyeShadowDistBtw,rightEyeShadowDistBtw)]


initVals= initialState()

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

    #up -> eyeshadow dist dec only and no need to cal. dist b/w uper lash and lower lash


    #down->blinkdetector use
    leftIrisCorner = detector.getLandMarkOf(0,474 ) #jisto use krke dist find krna
    leftEyeCorner = detector.getLandMarkOf(0,263)
    leftEyeDis,_ = cf.findDistance(leftIrisCorner,leftEyeCorner)
    print(leftEyeDis,end=' ')

    rightIrisCorner = detector.getLandMarkOf(0,471)
    rightEyeCorner = detector.getLandMarkOf(0,33)
    rightEyeDis,_ = cf.findDistance(rightEyeCorner,rightIrisCorner)
    print(rightEyeDis)

    leftEyeShadowUpper = detector.getLandMarkOf(0, 257)
    leftEyeShadowDown = detector.getLandMarkOf(0, 386)
    leftEyeShadowDistBtw,_ = cf.findDistance(leftEyeShadowUpper,leftEyeShadowDown)


    rightEyeShadowUpper = detector.getLandMarkOf(0, 27)
    rightEyeShadowDown = detector.getLandMarkOf(0, 159)
    rightEyeShadowDistBtw,_ = cf.findDistance(leftEyeShadowUpper,leftEyeShadowDown)



    if(initVals[0][0]>leftEyeDis): #left
        cv2.putText(img,"LEFT",(100,100),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255))
    else:
        pass
    if(initVals[0][1]>rightEyeDis): #right
        cv2.putText(img,"RIGHT",(100,200),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255))
    else:
        pass
    if(initVals[1][0]>leftEyeShadowDistBtw and initVals[1][1]>rightEyeShadowDistBtw):#up
        cv2.putText(img, "UP", (100, 150), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255))
    else:
        pass

    #down ka issue ki vo kahi blink na krde vali situation

    cv2.imshow("img",img)
    if(cv2.waitKey(1)==ord('q')):
        break