import calc
import stereo
import server
import time


s = stereo.Stereo(0,1)

server.startServer()

time.sleep(1)

while 1:
	s.find()
	server.putData((-1000,-1000),s.centerAngle, s.diagonalDist,0)
	print "angle: "+str(s.centerAngle)
	print "disto: "+str(s.distance)

