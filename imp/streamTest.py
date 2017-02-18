import gst_streamer as gs
import cv2

indexes =[2,-1,-1]
gs.start(indexes)

while 1:
    frame = gs.frame_peg
    cv2.imshow("peg", frame)
    cv2.waitKey(1)
