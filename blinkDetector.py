import cv2
import numpy as np

# import eyestrackingdetector as et

img_bgr =  cv2.imread("media/blinkDetection/query/righteyeblinked.jpg")
img_gray = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2GRAY)

righteyetemp = cv2.imread("media/blinkDetection/train/righteye.jpg",0)
w,h = righteyetemp.shape[::-1]

res = cv2.matchTemplate(img_gray,righteyetemp,cv2.TM_CCOEFF_NORMED)
threshlod = 0.65
loc = np.where(res>=threshlod)

for pt in zip(*loc[::-1]):
    cv2.rectangle(img_bgr,pt,(pt[0]+w,pt[1]+h),(0,255,255),2)

cv2.imshow("Detected",img_bgr)
cv2.waitKey(0)
# while True:
#     st,img = cam.read()
#
#     kp1,des1 = orb.detectAndCompute(img,None)

    ####capturing
    # leftEye,rightEye = detect.Process(img)

    #####

    ##det/recognition
    # cv2.drawKeypoints(trainimg,kp1,None)
    # cv2.imshow("original",trainimg)

    # cv2.imshow("left eye training img",trainimg)
    # if cv2.waitKey(1)== ord('q'):
    #     break