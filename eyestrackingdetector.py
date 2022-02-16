import cv2
import faceMesh as FM

class EyesTracker():

    def __init__(self):
        self.detector = FM.FaceDetector(maxFaces=1, refinedDetection=True)


    ############################### image query/detection #####################################
    def Process(self,img):
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.detector.Process(self.imgRGB)
        leftEyeUpr, leftEyeDown = self.detector.getLandMarkOf(0, 443), self.detector.getLandMarkOf(0, 450)
        leftEyeLeft, leftEyeRight = self.detector.getLandMarkOf(0,464), self.detector.getLandMarkOf(0,359)

        leftEyeHeight = (leftEyeUpr[1], leftEyeDown[1])
        leftEyeWidth = (leftEyeLeft[0], leftEyeRight[0])
        leftEyeCrop = img[leftEyeHeight[0]:leftEyeHeight[1], leftEyeWidth[0]:leftEyeWidth[1]]
        leftEyeCrop = cv2.resize(leftEyeCrop,(leftEyeWidth[1] - leftEyeWidth[0],leftEyeHeight[1] - leftEyeHeight[0]))

        rightEyeUpr,rightEyeDown = self.detector.getLandMarkOf(0,223),self.detector.getLandMarkOf(0,230)
        rightEyeLeft,rightEyeRight=self.detector.getLandMarkOf(0,130),self.detector.getLandMarkOf(0,244)
        rightEyeHeight = (rightEyeUpr[1],rightEyeDown[1])
        rightEyeWidth =  (rightEyeLeft[0],rightEyeRight[0])
        rightEyeCrop= img[rightEyeHeight[0]:rightEyeHeight[1],rightEyeWidth[0]:rightEyeWidth[1]]
        rightEyeCrop = cv2.resize(rightEyeCrop,(rightEyeWidth[1]-rightEyeWidth[0],rightEyeHeight[1]-rightEyeHeight[0]))

        return leftEyeCrop,rightEyeCrop
    #######################################################################################

    def show(self):
        while True:
            cv2.imshow("leftEyeCrop", self.leftEyeCrop)
            cv2.imshow("rightEyeCrop",self.rightEyeCrop)
            cv2.imshow("orignal",self.img)

            if cv2.waitKey(1)==ord('q'):
                break