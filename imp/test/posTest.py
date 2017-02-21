import position

pospx = position.getCurrentPositionPx(5, 200)
heading = position.getHeading(5, 200, 1)
angle = position.getTurnAngle(pospx, 1)

print "position: ",pospx
print "heading: ",heading
print "angle: ",angle

position.draw(pospx, 1)
