from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import argparse
import imutils
from collections import deque
import serial
import struct
ser=serial.Serial('/dev/ttyAMA0',9600)
ser.write('a')

ser.write('1')
time.sleep(1)
### construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v",
        help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
        help="max buffer size")
args = vars(ap.parse_args())
# define the lower and upper boundaries of the "yellow"
#Yellow Colour
#yellowLower = (25, 110, 110)
#yellowUpper = (30, 255, 255)
#Blue Colour 
yellowLower = (100, 50, 50)
yellowUpper = (130, 255, 255)
pts = deque(maxlen=args["buffer"])
camera=PiCamera()
camera.resolution=(640,480)
camera.framerate=32
rawCapture=PiRGBArray(camera, size=(640,480))
time.sleep(0.1)
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame=frame.array
# Start Image processing code
        #frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # construct a mask for the color "yellow", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, yellowLower, yellowUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        # only proceed if at least one contour was found
        if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                new_center= (center[0]/3, center[1]/3)
                new_center= ('%0*d' % (3,new_center[0]), '%0*d' % (3,new_center[1]))
                Ballx=center[0]/3
                Bally=center[1]/3
                Bally=160-Bally
                print "x:", Ballx
                print "y:", Bally
                if Ballx>=95 and Ballx<=115:
                        print "Object is in the middle of the camera"
                        ser.write('0')
                       # break
                # only proceed if the radius meets a minimum size
                if radius > 10:
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        cv2.circle(frame, (int(x), int(y)), int(radius),
                                (0, 255, 255), 2)
                        cv2.circle(frame, center, 5, (0, 0, 255), -1)
        # update the points queue
        pts.appendleft(center)
        # show the frame to our screen
        cv2.imshow("Frame", frame)
        rawCapture.truncate(0) 
        key = cv2.waitKey(1) & 0xFF
        ser.write('d')#Detach Servos 
                


        
        

        


    
  
