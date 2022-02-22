import math
import cv2
import commonfile as cf



def initialstate(cam,detector,distDetector,irisdetector):
    val={}

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
        rightEyeShadowDistBtw, _ = cf.findDistance(rightEyeShadowUpper,rightEyeShadowDown)


        ##########
        faceDist,_ =distDetector.Process(img)
        resiris = irisdetector.Process(img)


        val["EyeDistances"]=(leftEyeDis,rightEyeDis)
        val["EyeShadowsDistBtw"]=(leftEyeShadowDistBtw,rightEyeShadowDistBtw)
        val["FaceDist"] = faceDist


    return val