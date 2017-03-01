
import cv2
import numpy as np
import thread
#import fudge


class Stereo(object):

    def __init__(self, indexr, indexl): #right index, left index 

        self.hsvl = np.array((20,30,200))
        self.hsvh = np.array((90,255,255))

        #self.caps = [cv2.VideoCapture(camid0), cv2.VideoCapture(camid1)] #right, left

        self.cx = [-1, -1]
        self.cy = [-1, -1]
        self.err = [-1000, -1000] #right, left
        self.angles = [-1000, -1000] #right, left
        self.distance = -1000
        self.diagonalDist = -1000
        self.centerAngle = -1000
        self.distancer = -1000

        self.length = 8 #length b/w cams

        self.width = 800
        self.height = 448

        self.found = True

	self.minarea = 100

	pathr = "nvcamerasrc sensor-id="+str(indexr)+" ! queue max-size-buffers=0 max-size-bytes=0 max-size-time=0 ! video/x-raw(memory:NVMM), width=(int)448, height=(int)1080, format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=1  ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! videobalance brightness=-.6  !appsink name=sink"+str(indexr)
        self.piper = Gst.parse_launch(pathr)

        self.piper.set_state(Gst.State.PLAYING)
        self.appsinkr = self.pipe.get_by_name("sink"+str(indexr))
        self.appsinkr.set_property("emit-signals", True)
	self.appsinkr.set_property("max-buffers", 1)
	self.appsinkr.set_property("drop", True)

	pathl = "nvcamerasrc sensor-id="+str(indexl)+" ! queue max-size-buffers=0 max-size-bytes=0 max-size-time=0 ! video/x-raw(memory:NVMM), width=(int)448, height=(int)1080, format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=1  ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! videobalance brightness=-.6  !appsink name=sink"+str(indexl)
        self.pipe = Gst.parse_launch(pathl)

        self.pipel.set_state(Gst.State.PLAYING)
        self.appsinkl = self.pipe.get_by_name("sink"+str(indexl))
        self.appsinkl.set_property("emit-signals", True)
	self.appsinkl.set_property("max-buffers", 1)
	self.appsinkl.set_property("drop", True)


    def find(self, frameL, frameR): #frames passed in from gstreamer

        #_,frameL = self.caps[0].read()
        #_,frameR = self.caps[1].read()


	sampler = self.appsinkr.emit("pull-sample") ##problem##
        bufr = sampler.get_buffer()
        capsr = sampler.get_caps()

        frameR = np.ndarray((capsr.get_structure(0).get_value('height'),capsr.get_structure(0).get_value('width'),3),buffer=bufr.extract_dup(0, bufr.get_size()),dtype=np.uint8)


	samplel = self.appsinkl.emit("pull-sample") ##problem##
        bufl = samplel.get_buffer()
        capsl = samplel.get_caps()

        frameL = np.ndarray((capsl.get_structure(0).get_value('height'),capsl.get_structure(0).get_value('width'),3),buffer=bufl.extract_dup(0, bufl.get_size()),dtype=np.uint8)


        self.cx[0] = self.cx[1] = self.cy[0] = self.cy[1] = -1
        self.distance = self.diagonalDist = self.centerAngle = self.distancer = -1000
        self.angles[0] = self.angles[1] = -1000
        self.err[0] = self.err[1] = -600

        cv2.resize(frameL, (self.width, self.height))
        cv2.resize(frameR, (self.width, self.height))

        hsvL = cv2.cvtColor(frameL, cv2.COLOR_BGR2HSV)
        hsvR = cv2.cvtColor(frameR, cv2.COLOR_BGR2HSV)
        threshL = cv2.inRange(hsvL, self.hsvl, self.hsvh)
        threshR = cv2.inRange(hsvR, self.hsvl, self.hsvh)

        threshcpR = threshR.copy()
        threshcpL = threshL.copy()

        #find some contours
        contoursR,_ = cv2.findContours(threshR, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        contoursL,_ = cv2.findContours(threshL, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


        #grab the two biggest areas
        contoursR = sorted(contoursR, key=cv2.contourArea, reverse = True)[:2]
        contoursL = sorted(contoursL, key=cv2.contourArea, reverse = True)[:2]


        for cnt in contoursR:

	    if cv2.contourArea(cnt) < self.minarea:
	        self.cx[0] = -1
            	self.cy[0] = -1
    		self.found = False
    		break;

    	    M1 = cv2.moments(cnt)
            x,y = int(M1['m10']/M1['m00']), int(M1['m01']/M1['m00'])

    	    self.cx[0] += x
    	    self.cy[0] += y


    	for cnt in contoursL:

    	    if cv2.contourArea(cnt) < self.minarea:
                self.cx[1] = -1
                self.cy[1] = -1
                self.found = False
                break;

            M1 = cv2.moments(cnt)
            x,y = int(M1['m10']/M1['m00']), int(M1['m01']/M1['m00'])

            self.cx[1] += x
            self.cy[1] += y


    	self.cx[0] = (self.cx[0]+1)/2
    	self.cx[1] = (self.cx[1]+1)/2
    	self.cy[0] = (self.cy[0]+1)/2
    	self.cy[1] = (self.cy[1]+1)/2

        self.err[0] = self.cx[0]-(self.width/2)
        self.err[1] = self.cx[1]-(self.width/2)


        if self.found:
            self.angles[0] = calc.getAngle(self.err[0])
            self.angles[1] = calc.getAngle(self.err[1])
            self.distance = calc.getDist(self.err[0], self.err[1], self.length)
            #self.distancer = fudge.addFudge(self.distance)
            self.centerAngle = calc.getCenterAngle(self.angles[0], self.angles[1], self.distancer)
            self.diagonalDist = calc.getDiagonalDistance(self.centerAngle, self.distancer)


    	if self.found:
            cv2.circle(frameR,(self.cx[0],self.cy[0]),5,255,-1)
    	    cv2.circle(frameL,(self.cx[1],self.cy[1]),5,255,-1)
            cv2.line(frameR,(self.cx[0],0),(self.cx[0],self.height),150,2)
            cv2.line(frameR,(400,0),(400,self.height),200,2)
            cv2.line(frameL,(self.cx[0],0),(self.cx[0],self.height),150,2)
            cv2.line(frameL,(400,0),(400,self.height),200,2)
            #cv2.circle(threshcp,(cx,cy),15,120,1)
            #cv2.line(threshcp,(cx,cy-17),(cx,cy+17),150,2)
            #cv2.line(threshcp,(cx-17,cy),(cx+17,cy),150,2)
            #cv2.line(frame,(cx,0),(cx,480),70,2)
            #cv2.line(frame,(0,cy),(640,cy),70,2)
    	self.found = True


    	#print "right ",cx[0]," ",cy[0]
    	#print "left ",cx[1]," ",cy[1]

        print self.distance," inches perpendicular"
        print self.diagonalDist," inches diagonal"
        print self.centerAngle," degrees from center"


        #dst = dst = cv2.addWeighted(frameR, 1.0, frameL, 1.0, 0)

    	#cv2.imshow("righthsv", threshcpR)
    	#cv2.imshow("lefthsv", threshcpL)
        cv2.imshow("merge", dst)
    	cv2.imshow("right", frameR)
    	cv2.imshow("left", frameL)
    	cv2.waitKey(1)



lock = thread.allocate_lock()

def run(camid0, camid1):

    s = Stereo(camid0, camid1)
    while 1:
        with lock:
            s.find()


def start(camid0, camid1):
        thread.start_new_thread(run(camid0, camid1), ())


def stop():
    thread._stop.set()
