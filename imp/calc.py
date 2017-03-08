from __future__ import division
import math


fov = 53.5 #horizontal
maxwidth = 1920


def getAngle(error):

	err = error
	angle = 0.0

	angle = math.atan(err / 1904.61)
	angle = math.degrees(angle)
	angle = round(angle,2)

	return angle


def getPegAngle(error): #camera flipped on side

	err = error
	angle = 0.0

	angle = math.atan(err/1425.31)
	angle = math.degrees(angle)
	angle = round(angle,2)

	return angle




def getDist(errR, errL, len):

    if errL - errR == 0:
	return -1000
    return (len*maxwidth)/(2*math.tan(math.radians(fov/2))*(abs(errL-errR)))


def getCenterAngle(angR, angL, dist, length): #on ot pic

    #print "L: "+str(abs(angL))
    #print "R: "+str(abs(angR))

    if abs(angL) > abs(angR): #on the right
        theta = round(dist/((length/2)-(dist/math.tan(math.radians(90-angL)))),3)
    elif abs(angR) > abs(angL): #on the left
        theta = -1*round(dist/((length/2)-(dist/math.tan(math.radians(90-angR)))),3)
    elif angR == angL:
    	theta = 0 #dead on
    else:
        theta = -1000

    return theta


def getDiagonalDistance(angE, dist): #perp dist

	return dist/math.cos((math.radians(angE)))

