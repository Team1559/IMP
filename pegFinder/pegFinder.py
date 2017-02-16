import cv2
import numpy as np
import thread


class PegFinder(object):

    def __init__(self, camid):

        self.hsvl = np.array((60,30,200));
        self.hsvh = np.array((90,255,255));
        self.minarea = 10
        self.found = True

        self.cap = cv2.VideoCapture(camid)

        self.cx = -1
        self.cy = -1


    def find(self):

        while 1:

        	#grab some frames
        	_,frame = self.cap.read()

        	self.cx = self.cy = -1

        	#convert to hsv
        	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        	thresh = cv2.inRange(hsv, self.hsvl, self.hsvh)
        	threshcp = thresh.copy()

        	#find some contours
        	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        	#grab the two biggest areas
        	contours = sorted(contours, key=cv2.contourArea, reverse = True)[:2]

        	#find centroids of contours
        	i = 0
        	for cnt in contours:

        		if cv2.contourArea(cnt) < minarea:
        			self.cx = self.cy = -1
        			self.found = False
        			break;


        		M1 = cv2.moments(cnt)
        		x1,y1 = int(M1['m10']/M1['m00']), int(M1['m01']/M1['m00'])


        		self.cx += x1
        		self.cy += y1

        		print cx," ",cy

        	self.cx = (self.cx+1)/2
        	self.cy = (self.cy+1)/2

        	#draw it
        	if self.found:
                	cv2.circle(frame,(cx,cy),5,255,-1)
        	self.found = True

        	#show the image
        	cv2.imshow("thresh", threshcp)
        	cv2.imshow("frame", frame)
        	cv2.waitKey(1)



lock = thread.allocate_lock()

def run(camid):

    p = PegFinder(camid)
    while 1:
        with lock:
            p.find()


def start(camid):
        thread.start_new_thread(run(camid), ())


def stop():
    thread._stop.set()
