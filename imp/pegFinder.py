import cv2
import numpy as np
import thread
import calc
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst


class PegFinder(object):

    def __init__(self, index, showImage): #camera index (for gstreamer)

        self.hsvl = np.array((30,0,0))
        self.hsvh = np.array((75,255,255))
	#self.hsvl = np.array((0,0,150)) #low hsv values for RED
	#self.hsvh = np.array((15,255,255)) #high hsv values for RED

        self.minarea = 100
        self.found = True

        #self.cap = cv2.VideoCapture(camid)

        self.cx = -1
        self.cy = -1

        self.err = -1000

        self.angle = -1000

	self.found = True

	#changed because camera on side
        self.height = 1080
        self.width = 448

	#self.frame = np.zeros((800,448,3), np.uint8)

	self.showImage = showImage


	Gst.init(None)

	#camera mounted on side
        path = "nvcamerasrc sensor-id="+str(index)+" ! queue max-size-buffers=0 max-size-bytes=0 max-size-time=0 ! video/x-raw(memory:NVMM), width=(int)448, height=(int)1080, format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=1  ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! videobalance brightness=-.6  !appsink name=sink"+str(index)
        self.pipe = Gst.parse_launch(path)

        self.pipe.set_state(Gst.State.PLAYING)
        self.appsink = self.pipe.get_by_name("sink"+str(index))
        self.appsink.set_property("emit-signals", True)
	self.appsink.set_property("max-buffers", 1)
	self.appsink.set_property("drop", True)

        #self.frame = np.zeros((800,448,3), np.uint8) #black image


    def find(self): #frame passed in from gstreamer

	#print "ya mom"

    	#grab some frames
      	#_,frame = self.cap.read()

	#frame = gFrame

	sample = self.appsink.emit("pull-sample") ##problem##

        buf = sample.get_buffer()
        caps = sample.get_caps()

        frame = np.ndarray((caps.get_structure(0).get_value('height'),caps.get_structure(0).get_value('width'),3),buffer=buf.extract_dup(0, buf.get_size()),dtype=np.uint8)


       	self.cx = self.cy = -1
        self.err = -600 #-1000 when 400 subtracted
	self.angle = -1000

        #convert to hsv
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(hsv, self.hsvl, self.hsvh)
        threshcp = thresh.copy()

	#blur it
	thresh = cv2.blur(thresh, (5,5))

	#erode and dilate
	thresh = cv2.erode(thresh, (3,3))
	thresh = cv2.dilate(thresh, (3,3))

        #find some contours
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        #grab the two biggest areas
        contours = sorted(contours, key=cv2.contourArea, reverse = True)[:2]

        #find centroids of contours
        i = 0
        for cnt in contours:

		print cv2.contourArea(cnt)

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

        self.err = self.cx-(self.height/2) #height bc camera flipped on side


        if self.found:
            self.angle = calc.getPegAngle(self.err)


        #draw it
        if self.found:
            cv2.circle(frame,(self.cx,self.cy),5,255,-1)
        self.found = True

        #show the image
	if self.showImage:
        	cv2.imshow("thresh", threshcp)
        	cv2.imshow("frame", frame)
        	cv2.waitKey(1)



    def putData(self,img):
	self.frame = img


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
