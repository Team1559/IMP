import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import cv2
import numpy as np


Gst.init(None)
pipe = Gst.parse_launch("nvcamerasrc sensor-id=2 ! video/x-raw(memory:NVMM), width=(int)800, height=(int)448, format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=2  ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink name=sink")
pipe.set_state(Gst.State.PLAYING)
#pipe.set_state(Gst.State.READY)
appsink = pipe.get_by_name("sink")
appsink.set_property("emit-signals", True)
#print appsink.get_property("emit-signals")

#sample = appsink.emit("pull_sample")

while 1:

	sample = appsink.emit("pull-sample")
	#print sample

	buf = sample.get_buffer()
	caps = sample.get_caps()

	arr = np.ndarray((caps.get_structure(0).get_value('height'),caps.get_structure(0).get_value('width'),3),buffer=buf.extract_dup(0, buf.get_size()),dtype=np.uint8)


#mat = cv2.cv.fromarray(arr)
#frame = cv2.cvtColor(arr, cv2.cv.COLOR_GRAY2BGR)


#gst = "nvcamerasrc sensor-id=2 ! video/x-raw(memory:NVMM), format=(string)BGR ! appsink name=opencvsink"
#vc = cv2.VideoCapture(gst)


#_,frame = vc.read()


	cv2.imshow("frame", arr)
	cv2.waitKey(1)
