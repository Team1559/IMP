#!/usr/bin/env python

import pegFinder
import server
import sys


showImage = False

for arg in sys.argv:
    if arg == 'y':
        showImage = True
    elif arg.startswith("?") or arg == '--help':
        print 'y: show image \n n: do not show image \n if blank: does not show image'
    else:
        print 'unknown: "%s"' % arg



server.startServer()
p = pegFinder.PegFinder(1, showImage)

while 1:
	p.find()
	server.putData((-1000,-1000),p.angle,-1000,1)
	print "angle:"+str(p.angle)
	#print p.err
