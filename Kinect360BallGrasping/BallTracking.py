import numpy as np
from PIL import Image
import cv2
import freenect
import time
import math


#Manipulator WRT Kinect
xmwrtk=0;
ymwrtk=15;
zmwrtk=13;

#Kinect Parameters
minDistance = -10.0
scaleFactor = 0.0021
w=640.0
h=480.0

KinectAngle=0
#Tilt the Kinect
ctx = freenect.init()
dev = freenect.open_device(ctx, freenect.num_devices(ctx) - 1)
freenect.set_tilt_degs(dev, KinectAngle) #Min=-30, Max=30
dev=freenect.close_device(dev)
time.sleep(3)

# Define HSV Range of each Ball 
#BlUE COLOR
greenLower = (100, 50, 50)
greenUpper = (130, 255, 255)

#Yellow COLOR
#greenLower = (25, 110, 110)
#greenUpper = (30, 255, 255)

# Process Video
while True:
	# Start Kinect RGB and Depth Video
        KinectRGB,_=freenect.sync_get_video()
        KinectDepth,_=freenect.sync_get_depth(0, freenect.DEPTH_MM)
        
        # Grab Current Frame and Depth of the Ball
        frame= cv2.cvtColor(KinectRGB,cv2.COLOR_RGB2BGR)
        BallDepth=np.array(KinectDepth)
        
	#Blur, HSV and Mask Image
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	
	# find contours in the mask and initialize the current(x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use it to compute the centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		if radius > 10:

                        #Process X Y Z
                        zbwrtk=(BallDepth[y][x])*0.1
                        xbwrtk = (x - (w / 2.0)) * (zbwrtk + minDistance) * scaleFactor
                        ybwrtk = ((y - (h / 2.0)) * (zbwrtk + minDistance) * scaleFactor)*-1
                        print "XBwrtk:", xbwrtk, "cm"
                        print "YBwrtK:", ybwrtk, "cm"
                        print "ZBwrtK:", zbwrtk, "cm"
                     
                        
			# draw the circle and centroid on the frame,then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			karim=cv2.circle(frame, center, 5, (0, 0, 255), -1)
			break

#Save Images
depth,_ = freenect.sync_get_depth()
depth = depth.astype(np.uint8)
cv2.imwrite('rgb.png', frame)        
cv2.imwrite('depth.png',depth)
cv2.imwrite('mask.png',mask)

#Fnd Ball WRT Manipulator
xd=zbwrtk-zmwrtk
yd=xmwrtk-xbwrtk
zd=ybwrtk-ymwrtk

#Print Ball with Respect to Manipulator
print "XBwrtM:", xd, "cm"
print "YBwrtM:", yd, "cm"
print "ZBwrtM:", zd, "cm"

#Manipulator Actuation
#import Manipulator
#Manipulator.actuate(xd,yd,zd)

                        





































        

