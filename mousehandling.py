import pyautogui

wScr,hScr= pyautogui.size() #getting size of the window

def moveRight(estimatedDist):
    try:
        if(pyautogui.position()[0]>=0 and pyautogui.position()[0]<wScr):
            pyautogui.moveTo(pyautogui.position()[0]+estimatedDist, pyautogui.position()[1])
        else:
            pyautogui.moveTo(0,0)
    except:
        try:
            if pyautogui.position()[1] > hScr:
                pyautogui.moveTo(x=wScr,y=hScr-1)
            elif pyautogui.position()[1]<0:
                pyautogui.moveTo(x=wScr, y=1)
            else:
                pyautogui.moveTo(x=wScr,y=pyautogui.position()[1])
        except:
            print("move in the region")

def moveLeft(estimatedDist):
    try:
        if(pyautogui.position()[0]>=0 and pyautogui.position()[0]<wScr):
            pyautogui.moveTo(estimatedDist-pyautogui.position()[0], pyautogui.position()[1])
        else:
            pyautogui.moveTo(0,0)
    except:
        try:
            if pyautogui.position()[1] > hScr:
                pyautogui.moveTo(x=0,y=hScr-1)
            elif pyautogui.position()[1]<0:
                pyautogui.moveTo(x=0, y=1)
            else:
                pyautogui.moveTo(x=0,y=pyautogui.position()[1])
        except:
            print("move in the region")

    pass
def moveUp(estimatedDist):
    try:
        if(pyautogui.position()[1]>=0 and pyautogui.position()[1]<hScr):
            pyautogui.moveTo(pyautogui.position()[0], estimatedDist-pyautogui.position()[1])
        else:
            pyautogui.position(0,0)
    except:
        try:
            if pyautogui.position()[0] > wScr:
                pyautogui.moveTo(x=wScr-1, y=0)
            elif pyautogui.position()[0] < 0:
                pyautogui.moveTo(x=1, y=0)
            else:
                pyautogui.moveTo(x=pyautogui.position()[0], y=0)
        except:
            print("move in the region")


def moveDown(estimatedDist):
    try:
        if (pyautogui.position()[1] >= 0 and pyautogui.position()[1] < hScr):
            pyautogui.moveTo(pyautogui.position()[0],estimatedDist+pyautogui.position()[1])
        else:
            pyautogui.moveTo(0,0)
    except:
        try:
            if pyautogui.position()[0] > wScr:
                pyautogui.moveTo(x=wScr-1, y=hScr)
            elif pyautogui.position()[0] < 0:
                pyautogui.moveTo(x=1, y=hScr)
            else:
                pyautogui.moveTo(x=pyautogui.position()[0], y=hScr)
        except:
            print("move in the region")


def leftclick():
    pass
def rightclick():
    pass
def doubleClick():
    pass