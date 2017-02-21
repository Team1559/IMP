from multiprocessing import Process, Queue
from threading import Thread
import cv2
import pegFinder
import server
import gst_streamer as gs
import numpy as np
import time
import thread
import imgbuffer


#server.startServer()
#q = Queue()
p = pegFinder.PegFinder() #index
streamer = gs.Streamer(0) #index

#streamer.stream()
#time.sleep(1)
#p.find(streamer.frame)
#print p.cx
#time.sleep(1)


#lock = thread.allocate_lock()

#while 1:
#	p.find()


def find():
	while 1:
		#with lock:
#		streamer.stream()
		#cv2.imshow("",q.get())
		#cv2.waitKey(1)
		#print 1
		#print q.get()
		#p.find(q.get())
			#print p.cx
#		cv2.imshow("f",streamer.frame)
		p.find()

def stream():
	while 1:
		#with lock:
		#print "stream"
		streamer.stream()
		p.putData(streamer.frame)
		#imgbuffer.putData(streamer.frame)
		#q.put(streamer.frame)
		#q.put("hi")
		#print q



#while 1:
#	streamer.stream()


#Process(target=stream).start()
#Process(target=find).start()

t1 = Thread(target=stream)
t2 = Thread(target=find)

t1.start()
t2.start()


#while 1:
	#print "stream"
	#streamer.stream()

#Process(target=find).start()

#thread.start_new_thread(stream,())
#thread.start_new_thread(find,())


#while 1:
    #streamer.stream()
    #frame = streamer.frame
    #p.find(streamer.frame)
    #cv2.imshow("peg", frame)
    #cv2.waitKey(1)
    #p.find()
    #server.putData(-1000,p.angle,-1000,1)
