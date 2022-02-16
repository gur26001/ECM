import cv2
import faceMesh as FM
import time
cam = cv2.VideoCapture(0)
cam.set(3,640)
cam.set(4,480)

detector = FM.FaceDetector(refinedDetection=True)

#upper outline, upper innerline, bottom innerline
LEFT_EYE = [257,[398,384,385,386,387,388,466],[382,281,249,390,373,374,280]]
rightList=[27,[246,161,160,159,158,157,173],[55,54,53,45,44,63,7]]
# rightList = [33,7,163,144,145,153,154,155,133,173,157,158,159,160,161,246]
count=0



def initBlinkState():
    for i in range(0,2):
        status, img = cam.read()
        imgRGB= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        detector.Process(imgRGB)
        rightUp = detector.getLandMarkOf(0,159)
        rightDown = detector.getLandMarkOf(0,145)

    return rightUp[1],rightDown[1]

initialRightUppery,initialRightDowny = initBlinkState()

blinkCounter=0
currRightUppery, currRightDowny = detector.getLandMarkOf(0,159)[1],detector.getLandMarkOf(0,23)[1]
while cam.isOpened():
    status,img = cam.read()
    # img= cv2.flip(img,1)
    imgRGB= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    detector.Process(imgRGB)


    cv2.circle(img,detector.getLandMarkOf(0,386),1,(0,255,0),-1)
    cv2.circle(img, detector.getLandMarkOf(0,374), 1, (0, 255, 255), -1)
    # cv2.circle(img,detector.getLandMarkOf(0,159),1,(0,255,0),-1)
    # cv2.circle(img, detector.getLandMarkOf(0, 145), 1, (0, 255, 255), -1)

    prevRightUppery, prevRightDowny = currRightUppery, currRightDowny
    currRightUppery, currRightDowny = detector.getLandMarkOf(0,159)[1],detector.getLandMarkOf(0,145)[1]
    # cv2.line(img,rightUp,rightDown,(0,255,0),2)
    # cv2.line(img, rightLeft, rightRight, (0, 255, 0), 2)

    if((currRightUppery>prevRightUppery and currRightDowny<prevRightDowny)):
        blinkCounter+=1
        print("Blinked")

    cv2.imshow("img",img)

    if (cv2.waitKey(1)==ord('q')):
        break

print(blinkCounter)