import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import numpy as np
import thread



class Streamer(object):

    def __init__(self, index):

        #rear peg cam, stereo ones
        #sinks are sink+index, ex) sink0
        self.pipes = [Gst.parse_launch("nvcamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=(int)800, height=(int)448, format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=2  ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink name=sink0"),
                      Gst.parse_launch("nvcamerasrc sensor-id=1 ! video/x-raw(memory:NVMM), width=(int)800, height=(int)448, format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=2  ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink name=sink1"),
                      Gst.parse_launch("nvcamerasrc sensor-id=2 ! video/x-raw(memory:NVMM), width=(int)800, height=(int)448, format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=2  ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink name=sink2")]

        #self.i = 0
        #for pipe in self.pipes:
        self.pipes[index].set_state(Gst.State.Playing)
        self.appsink = pipe.get_by_name("sink"+i)
        self.appsink.set_property("emit-signals", True)
            #self.i = self.i + 1

        self.frame = None

        self.camindex = index

    def stream(self):

        sample = self.appsink[self.camindex].emit("pull-sample")

    	buf = sample.get_buffer()
    	caps = sample.get_caps()

    	arr = np.ndarray((caps.get_structure(0).get_value('height'),caps.get_structure(0).get_value('width'),3),buffer=buf.extract_dup(0, buf.get_size()),dtype=np.uint8)
        self.frame = arr



global frame_peg, frame_right, frame_left
frame_peg = None
frame_right = None
frame_left = None

lock = thread.allocate_lock()

camidlist = ["peg", "r", "l"]


def start(indexes): #list of indexes of peg, right, left

    for index, i in enumerate(indexes):
        if i == -1:
            thread.start_new_thread(run,(indexes[i], camidlist[index]))



def run(index, id):

    if id is "peg":
        s = Streamer(index)
        while 1:
            with lock:
                frame_peg = s.frame

    elif id is "r":
        s = Streamer(index)
        while 1:
            with lock:
                frame_right = s.frame

    elif id is "l":
        s = Streamer(index)
        while 1:
            with lock:
                frame_left = s.frame
