from multiprocessing import Process
import cv2
import pegFinder
import server
import gst_streamer as gs
import numpy as np


server.startServer()
p = pegFinder.PegFinder()
streamer = gs.Streamer(1) #index 1


def find():
	while 1:
		streamer.stream()
		p.find(streamer.frame)

def stream():
	while 1:
		streamer.stream()



Process(target=stream).start()
Process(target=find).start()



while 1:
    server.putData(-1000,p.angle,-1000,1)
