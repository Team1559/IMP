
from __future__ import division
import numpy as np
import math
import cv2


pegs = [(330,170), (295,225), (330,275)] #px
boiler = [190, 405] #px

pxPerIn = 405/323.75


def pxToIn(px):
    return px/pxPerIn

def inToPx(inch):
    return inch*pxPerIn


def getCurrentPositionPx(angE, dist):

    x = math.sin(math.radians(angE))*inToPx(dist)
    y = math.cos(math.radians(angE))*inToPx(dist)

    return (int(x)+boiler[0], boiler[1]-int(y))


def getHeadingPx(pegid, pospx):

    dx = pegs[pegid][0] - pospx[0]
    dy = pospx[1] - pegs[pegid][1]

    return (int(dx), int(dy))


def getTurnAngle(pospx, pegid): #angle to get to perpendicular

    if pospx[1] < pegs[pegid][1]: #above it, turn right
        theta = round((math.degrees(math.atan((pegs[pegid][1]+pospx[1])/(pegs[pegid][0]+pospx[0])))),3)
    elif pospx[1] > pegs[pegid][1]: #below it, turn left
        theta = -1*round((math.degrees(math.atan((pegs[pegid][1]+pospx[1])/(pegs[pegid][0]+pospx[0])))),3)

    return theta


def getHeading(angE, dist, pegid):

    pos = getCurrentPositionPx(angE, dist)
    headingpx = getHeadingPx(pegid, pos)

    return (pxToIn(headingpx[0]), pxToIn(headingpx[1]))


def draw(pospx, pegid):

    img = cv2.imread("Field.PNG")
    cv2.circle(img, (pospx[0],pospx[1]),15,(100,250,175),-1)
    cv2.line(img,(boiler[0],boiler[1]),(pospx[0],pospx[1]),(50,100,150),5)
    cv2.line(img,(pospx[0],pospx[1]),(pegs[pegid][0],pegs[pegid][1]),(50,150,200),5)

    cv2.imshow("field", img)
    cv2.waitKey(0)


def reasons_to_live():
    return None
