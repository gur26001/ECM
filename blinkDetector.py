import cv2
import faceMesh as FM


detector= FM.FaceDetector(maxFaces=1,refinedDetection=True)
cam = cv2.VideoCapture(0)

while True:
    st,img= cam.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    detector.Process(imgRGB)

    ############################### image query/detection #####################################
    leftEyeUpr, leftEyeDown = detector.getLandMarkOf(0, 443), detector.getLandMarkOf(0, 450)
    leftEyeLeft, leftEyeRight = detector.getLandMarkOf(0,464), detector.getLandMarkOf(0,359)

    leftEyeHeight = (leftEyeUpr[1], leftEyeDown[1])
    leftEyeWidth = (leftEyeLeft[0], leftEyeRight[0])
    leftEyeCrop = img[leftEyeHeight[0]:leftEyeHeight[1], leftEyeWidth[0]:leftEyeWidth[1]]
    leftEyeCrop = cv2.resize(leftEyeCrop,(leftEyeWidth[1] - leftEyeWidth[0],leftEyeHeight[1] - leftEyeHeight[0]))

    rightEyeUpr,rightEyeDown = detector.getLandMarkOf(0,223),detector.getLandMarkOf(0,230)
    rightEyeLeft,rightEyeRight=detector.getLandMarkOf(0,130),detector.getLandMarkOf(0,244)
    rightEyeHeight = (rightEyeUpr[1],rightEyeDown[1])
    rightEyeWidth =  (rightEyeLeft[0],rightEyeRight[0])
    rightEyeCrop= img[rightEyeHeight[0]:rightEyeHeight[1],rightEyeWidth[0]:rightEyeWidth[1]]
    rightEyeCrop = cv2.resize(rightEyeCrop,(rightEyeWidth[1]-rightEyeWidth[0],rightEyeHeight[1]-rightEyeHeight[0]))

    cv2.imshow("leftEyeCrop",leftEyeCrop)
    cv2.imshow("rightEyeCrop",rightEyeCrop)

    #######################################################################################



    cv2.imshow("orignal",img)

    if cv2.waitKey(1)==ord('q'):
        break