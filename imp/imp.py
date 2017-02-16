from multiprocessing import Process
import cv2
import position
import pegFinder
import stereo
import server

###IMPLEMENT GETTING FRAMES FROM GSTREAMER###
###^^^PUT GRABBING FRAMES IN OWN PROCESS^^^###

def stereo():
    s = stereo.Stereo(1,0)
    while 1:
        s.find()

def peg():
    p = pegFinder.PegFinder(3)
    while 1:
        p.find()

Process(target=stereo).start()
Process(target=peg).start()

server.startServer()

while 1:
    heading = position.getHeading(s.centerAngle,s.diagonalDist,0)
    server.putData(heading,s.centerAngle,s.diagonalDist,0)
