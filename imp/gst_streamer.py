from multiprocessing import Process
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import numpy as np
import thread
import cv2
import pegFinder



class Streamer(object):

    def __init__(self, index):

        Gst.init(None)

        #rear peg cam, stereo ones
        #sinks are sink+index, ex) sink0
        path = "nvcamerasrc sensor-id="+str(index)+" ! queue max-size-buffers=0 max-size-bytes=0 max-size-time=0 ! video/x-raw(memory:NVMM), width=(int)800, height=(int)1080, format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=1  ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink name=sink"+str(index)
        self.pipe = Gst.parse_launch(path)

        #self.i = 0
        #for pipe in self.pipes:
        self.pipe.set_state(Gst.State.PLAYING)
        self.appsink = self.pipe.get_by_name("sink"+str(index))
        self.appsink.set_property("emit-signals", True)
            #self.i = self.i + 1
	self.appsink.set_property("drop", True)
	self.appsink.set_property("max-buffers", 1)

        self.frame = np.zeros((800,448,3), np.uint8) #black image

        self.camindex = index

	#print index

	#self.peg = pegFinder.PegFinder()


    def stream(self):

	#self.pipe.set_state(Gst.State.PLAYING)
	#print self.appsink.get_property("emit-signals")

        sample = self.appsink.emit("pull-sample") ##problem##

	#print sample

        buf = sample.get_buffer()
        caps = sample.get_caps()

        self.frame = np.ndarray((caps.get_structure(0).get_value('height'),caps.get_structure(0).get_value('width'),3),buffer=buf.extract_dup(0, buf.get_size()),dtype=np.uint8)
        #self.frame = arr

	#self.peg.find(self.frame)	


class Manager(object):

    def __init__(self, indexes): #list of indexes of peg, right, left

        self.frame_peg = np.zeros((800,448,3), np.uint8) #black image
        self.frame_right = np.zeros((800,448,3), np.uint8)
        self.frame_left = np.zeros((800,448,3), np.uint8)

        self.lock = thread.allocate_lock()

        self.camidlist = ["peg", "r", "l"]

        self.indexes = indexes



    def start(self):

        for index, i in enumerate(self.indexes):
            if i != -1:
		#print self.camidlist[index]
                thread.start_new_thread(self.run,(i, self.camidlist[index]))
		#Process(target=self.run, args=(i,self.camidlist[index])).start()



    def run(self, index, camid):

        print "running"

        if camid == "peg":
            s = Streamer(index)
	    #print "peg"
            while 1:
                with self.lock:
		    #print "peg"
                    s.stream()
                    self.frame_peg = s.frame
	            #cv2.imshow("",frame_peg)
       	            #cv2.waitKey(1)

        elif camid == "r":
            s = Streamer(index)
            while 1:
                with self.lock:
                    s.stream()
                    self.frame_right = s.frame

        elif camid == "l":
            s = Streamer(index)
            while 1:
                with self.lock:
                    s.stream()
                    self.frame_left = s.frame


