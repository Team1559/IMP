import gst_streamer as gs
import cv2
#import time

indices =[0,-1,-1]
#manager = gs.Manager(indexes)
#manager.start()

peg = gs.Streamer(indices[0])


while 1:
    peg.stream()
    frame = peg.frame
    cv2.imshow("peg", frame)
    cv2.waitKey(1)
