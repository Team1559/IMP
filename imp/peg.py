import cv2
import pegFinder
import server


camid = 2 #/dev/vide02


server.startServer()
p = pegFinder(camid)

while 1:
    p.find()
    server.putData(-1000,s.angle,-1000,1)
