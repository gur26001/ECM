import cv2
import faceMesh as FM
import math
import irisdetection as irisd
import commonfile as cf

class DistanceDetector():

    def __init__(self):
        self.detector = FM.FaceDetector(refinedDetection=True)
        self.f = 260    #focal length of camera
        self.W = 11.9   #avg The distance from the outer corners of the eyes (right and left ectocanthi)
        self.irisdetector = irisd.IrisDetector()
    def findDistance(self,p1, p2,img=None):  # logic and code from cvZone (i copy pasted due to easy of this project , because initially i have used directly mediapipe's facemesh)
        x1, y1 = p1
        x2, y2 = p2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)
        return length, (cx, cy)

    def Process(self,img):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.detector.Process(imgRGB)
        irises = self.irisdetector.Process(img)

        pointLeft = cf.findDistance(self.detector.getLandMarkOf(0,173),self.detector.getLandMarkOf(0,133))
        pointRight =cf.findDistance(self.detector.getLandMarkOf(0,398), self.detector.getLandMarkOf(0,362))

        w, cs = self.findDistance(pointLeft, pointRight) #exact between face

        currFaceDist = (self.W * self.f) / w

        return currFaceDist,(pointLeft,pointRight)