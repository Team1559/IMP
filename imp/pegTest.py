import pegFinder
import server


server.startServer()
p = pegFinder.PegFinder(1)

while 1:
	p.find()
	server.putData((-1000,-1000),p.angle,-1000,1)
	print p.angle
