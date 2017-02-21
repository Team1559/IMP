import sys
import cv2


data = None

def putData(x):
	global data
	data = x

def getData():
	global data
	return data 
