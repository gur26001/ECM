import cv2
import mediapipe as mp

class FaceDetector:
    FACE = []
    def __init__(self,maxFaces=1,refinedDetection=False,mindetect=0.5,mintrack=0.5):
        self.myFaceMesh = mp.solutions.face_mesh
        self.facemesh = self.myFaceMesh.FaceMesh(max_num_faces=maxFaces,refine_landmarks=refinedDetection,min_detection_confidence=mindetect,min_tracking_confidence=mintrack)

    def Process(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.facemesh.process(imgRGB)
        FACES = []
        if results.multi_face_landmarks:
            for id, faceLms in enumerate(results.multi_face_landmarks):
                LANDMARKS = {}
                for id, lm in enumerate(faceLms.landmark):
                    ih, iw, c = img.shape
                    x, y = int(lm.x * iw), int(lm.y * ih)
                    LANDMARKS[id] = (x, y)
                FACES.append(LANDMARKS)
        self.FACE = FACES
        return self.FACE
    def getLandMarkOf(self,FACENO, LandmarkNum):  # FACE NO MEANS-> INDEX OF FACES,FIRST SECOND... FACE
        return self.FACE[FACENO][LandmarkNum]     # returns TUPLE OF COORDINATES e.g. you called getLandMarkOf(0,145) =>returns (100,100)


