import math
def findDistance(p1, p2,img=None):  # logic and code from cvZone (i copy pasted due to easy of this project , because initially i have used directly mediapipe's facemesh)
    x1, y1 = p1
    x2, y2 = p2
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    length = math.hypot(x2 - x1, y2 - y1)
    return length, (cx, cy)
