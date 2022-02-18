#assuming initaily not blinked eye  or couldn't detect
    #before running you need to see in the middle of the screen  or couldn't detect
    #with glasses some errors may occur or couldn't detect

import cv2
import numpy as np
import  faceMesh as FM


def initialState():
    cam = cv2.VideoCapture(0)
    idetector = FM.FaceDetector()
    for i in range(0, 2):
        istat, iimg = cam.read()

        idetector.Process(iimg)

        ileftupperupper = idetector.getLandMarkOf(0, 257)
        ileftupperdown = idetector.getLandMarkOf(0, 386)

        ileftEyeShadowDist = ileftupperdown[1] - ileftupperupper[1]

        # ileftdownupper = idetector.getLandMarkOf(0, 374)
        # ileftUpperLidLowerLidDist = ileftdownupper[1] - ileftupperdown[1]

        irightupperupper = idetector.getLandMarkOf(0, 27)
        irightupperdown = idetector.getLandMarkOf(0, 159)

        irightEyeShadowDist = irightupperdown[1] - irightupperupper[1]

        # irightdownupper = idetector.getLandMarkOf(0, 145)
        # irightUpperLidLowerLidDist = irightdownupper[1] - irightupperdown[1]

        return (ileftEyeShadowDist, irightEyeShadowDist)


class BlinkDetector():

    def __init__(self):
        self.Count = [0, 0]  # leftblinkcount,rightblinkcount
        self.detector = FM.FaceDetector(refinedDetection=True)
        self.eyeblinkedDiffRange = range(1, 10)
        self.initialVals = initialState()

    def Process(self,img):

        self.detector.Process(img)

        leftupperupper= self.detector.getLandMarkOf(0,257)
        leftupperdown = self.detector.getLandMarkOf(0,386)

        leftEyeShadowDist = leftupperdown[1] - leftupperupper[1] ##

        leftdownupper = self.detector.getLandMarkOf(0,374)

        leftUpperLidLowerLidDist  = leftdownupper[1]-leftupperdown[1] ##

        # print("left->",leftHeightDiff,"leftdown->",leftHeightDiffBlink,end=' ')

        # cv2.circle(img, (leftupperupper), 1, (0, 255, 0))
        # cv2.circle(img, (leftupperdown), 1, (0, 255, 20))
        # cv2.circle(img, (leftdownupper), 1, (0, 255, 20))

        rightupperupper = self.detector.getLandMarkOf(0,27)
        rightupperdown = self.detector.getLandMarkOf(0, 159)

        rightEyeShadowDist = rightupperdown[1]-rightupperupper[1]   ##

        rightdownupper = self.detector.getLandMarkOf(0,145)

        rightUpperLidLowerLidDist = rightdownupper[1] - rightupperdown[1] ##

        # print("right->",rightHeightDiff,"rightdown",rightHeightDiffBlink)

        # cv2.circle(img,(rightupperupper),1,(0,255,0))
        # cv2.circle(img, (rightupperdown), 1, (0, 255, 20))
        # cv2.circle(img, (rightdownupper), 1, (0, 255, 20))

        #LEFT EYE BLINK DETECTION
        prevl = self.initialVals[0]
        if((prevl<leftEyeShadowDist) and (leftUpperLidLowerLidDist in self.eyeblinkedDiffRange)):
            # cv2.putText(img,"Left Blinked",(10,10),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0))
            self.Count[0] += 1

        #RIGHT EYE BLINK DETECTION
        prevr= self.initialVals[1]
        if ((prevr<rightEyeShadowDist) and (rightUpperLidLowerLidDist in self.eyeblinkedDiffRange)):
            # cv2.putText(img, "Right Blinked", (10, 80), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255))
            self.Count[1] += 1

        #showing
        #
        # cv2.imshow("orignal",img)
        #
        # if cv2.waitKey(1)== ord('q'):
        #     break
        #
        return  self.Count





#left eye blinked if Count[0] is not zero and Count[1] is zero -> left click
#right eye blinked if Count[1] is not zero and Count[0] is zero -> right click
#if both are non zero,no action
#it has one issue-> we can use number of 1 and 2 called to detect more than one click