from threading import Thread
from multiprocessing import Process
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import pegFinder
import gst_streamer as gs
import numpy as np
import cv2
import thread
import sys


Gst.init(None)
#(memory:NVMM) ! nvvidconv flip-method=2
pipe = Gst.parse_launch("nvcamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=(int)800, height=(int)448, format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=2 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink name=sink")
pipe.set_state(Gst.State.PLAYING)
appsink = pipe.get_by_name("sink")
appsink.set_property("emit-signals", True)

global frame
frame = np.zeros((800,448,3), np.uint8)


p = pegFinder.PegFinder()

def find():
	while 1:
		#print "ya mom"
		global frame
		p.find(frame)
		#cv2.imshow("",frame)
		#cv2.waitKey(1)


def stream():

	while 1:

		#print "ya"


		#pipe = Gst.parse_launch("nvcamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=(int)800, height=(int)448, format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=2  ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink name=sink")
		#pipe.set_state(Gst.State.PLAYING)
		#appsink = pipe.get_by_name("sink")
		#appsink.set_property("emit-signals", True)

		#print appsink
		sample = appsink.emit("pull-sample") ##problem##

        	buf = sample.get_buffer()
        	caps = sample.get_caps()

		global frame
        	frame = np.ndarray((caps.get_structure(0).get_value('height'),caps.get_structure(0).get_value('width'),3),buffer=buf.extract_dup(0, buf.get_size()),dtype=np.uint8)

		#cv2.imshow("", frame)
		#cv2.waitKey(1)

		#p.putData(frame)


if __name__ == '__main__':
	t = Thread(target=find)
	t2 = Thread(target=stream)
	t.start()
	#t.join()
	t2.start()

	#sys.stdout.flush()
	#thread.start_new_thread(stream,())
	#thread.start_new_thread(find, ())

	#t.join()
	#t2.join()

