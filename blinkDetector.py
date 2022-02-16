import cv2
import numpy as np

import eyestrackingdetector as et


cam = cv2.VideoCapture(0)
detect = et.EyesTracker()

Count=[0,0] #leftblinkcount,rightblinkcount
flagl,flagr=0,0

locLeft,locRight = np.array([]),np.array([])

while True:
    st,img = cam.read()
    leftEye, rightEye = detect.Process(img)

    ###capturing
    leftimggray = cv2.cvtColor(leftEye, cv2.COLOR_BGR2GRAY)
    rightimggray = cv2.cvtColor(rightEye, cv2.COLOR_BGR2GRAY)


    ###getting training images/ templates to search for , blink detection jisse krna he  to compare
    lefteyetemp = cv2.imread("media/blinkDetection/train/lefteye2.png",0)
    lw,lh = lefteyetemp.shape[::-1]
    righteyetemp = cv2.imread("media/blinkDetection/train/righteye2.jpg", 0)
    rw, rh = righteyetemp.shape[::-1]


    #recognition

    resLeft = cv2.matchTemplate(leftimggray,lefteyetemp,cv2.TM_CCOEFF_NORMED)
    threshlodL = 0.69
    locLeft = np.where(resLeft>=threshlodL)

    resRight = cv2.matchTemplate(rightimggray, righteyetemp, cv2.TM_CCOEFF_NORMED)
    threshlodR = 0.69
    locRight = np.where(resRight >= threshlodR)

    ptlc = 0
    for ptl in zip(*locLeft[::-1]):
        cv2.rectangle(leftEye, ptl, (ptl[0] + rw, ptl[1] + rh), (255,0 , 255), 2)
        ptlc+=1
        if (ptlc == 4):
            Count[0] += 1

    ptrc = 0
    for ptr in zip(*locRight[::-1]):
        cv2.rectangle(rightEye, ptr, (ptr[0] + rw, ptr[1] + rh), (0, 255, 255), 2)
        ptrc+=1

        if (ptrc==4):
            Count[1] += 1

    #showing
    # cv2.imshow("Left eye", leftEye)
    # cv2.imshow("Right eye",rightEye)
    cv2.imshow("orignal",img)

    if cv2.waitKey(1)== ord('q'):
        break


print(Count)