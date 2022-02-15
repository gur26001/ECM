import cv2
import mediapipe as mp
import numpy as np

# LEFT_EYE = [362,382,381,380,374,373,390,249,263,466,388,387,385,384,398]
# RIGHT_EYE = [33,7,163,144,145,153,154,155,133,173,157,158,159,160,161,246]
LEFT_IRIS = [474,475,476,477]
RIGHT_IRIS = [469,470,471,472]


class IrisDetector():

    IRISES=[]
    def __init__(self):
        myFaceMesh = mp.solutions.face_mesh

    def process(self,img): #returns the coordinates of the both iris and their radiuses
        with self.myFaceMesh.FaceMesh(max_num_faces=1,refine_landmarks=True,min_detection_confidence=0.5,min_tracking_confidence=0.5) as facemesh :
            imgRGB= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            ih,iw,cg = img.shape #ignoring color channels to get width and height
            results= facemesh.process(imgRGB)
            if results.multi_face_landmarks:
                # for i in (0,len(results.multi_face_landmarks)):
                # IRIS=[]
                meshpoints=np.array([np.multiply([p.x,p.y],[iw,ih]).astype(int) for p in results.multi_face_landmarks[0].landmark])
                (l_cx, l_cy), l_radius = cv2.minEnclosingCircle(meshpoints[LEFT_IRIS])  #to get the centre of iris but n floating nums
                (r_cx,r_cy), r_radius = cv2.minEnclosingCircle(meshpoints[RIGHT_IRIS])

                center_left = np.array([l_cx,l_cy],dtype=np.int32) #origin coordinates of left iris in int
                center_right = np.array([r_cx, r_cy], dtype=np.int32) #origin coordinates of right iris in int

                self.IRISES.append((center_left,center_right,l_radius,r_radius))

