import cv2
import numpy as np
import thread
import calc


class PegFinder(object):

    def __init__(self): #frame passed in from gstreamer (replaced camid and VideoCapture)

        #self.hsvl = np.array((60,30,200))
        #self.hsvh = np.array((90,255,255))
	self.hsvl = np.array((0,0,150)) #low hsv values for RED
	self.hsvl = np.array((15,255,255)) #high hsv values for RED

        self.minarea = 10
        self.found = True

        #self.cap = cv2.VideoCapture(camid)

        self.cx = -1
        self.cy = -1

        self.err = -1000

        self.angle = -1000

        self.height = 448
        self.width = 800


    def find(self, gframe): #frame passed in from gstreamer


    	#grab some frames
      	#_,frame = self.cap.read()

	frame = gframe

       	self.cx = self.cy = -1
        self.err = -600 #-1000 when 400 subtracted

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

        	if cv2.contourArea(cnt) < self.minarea:
        		self.cx = self.cy = -1
        		self.found = False
        		break;


        	M1 = cv2.moments(cnt)
        	x1,y1 = int(M1['m10']/M1['m00']), int(M1['m01']/M1['m00'])


        	self.cx += x1
        	self.cy += y1

        	#print cx," ",cy

	self.cx = (self.cx+1)/2
  	self.cy = (self.cy+1)/2

        self.err = self.cx-(self.width/2)

        if self.found:
            self.angle = calc.getAngle(self.err)


        #draw it
        if self.found:
            cv2.circle(frame,(self.cx,self.cy),5,255,-1)
        self.found = True

        #show the image
        #cv2.imshow("thresh", threshcp)
        #cv2.imshow("frame", frame)
        #cv2.waitKey(1)



##threading replaced with new process in main script##
lock = thread.allocate_lock()

def run():

    p = PegFinder()
    while 1:
        with lock:
            p.find()


def start():
        thread.start_new_thread(run, ())


def stop():
    thread._stop.set()
