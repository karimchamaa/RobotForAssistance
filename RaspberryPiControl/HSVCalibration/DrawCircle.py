import cv2
import numpy as np
import time
from time import sleep
import picamera
import math
import array
import PIL
import numpy
from PIL import Image
from PIL import ImageFilter

with picamera.PiCamera() as camera:
        camera.resolution=(2592,1944)
        camera.start_preview()
        sleep(10)
        camera.capture('Capture4.png')
        camera.stop_preview()
        im=Image.open('Capture4.png')

img = cv2.imread('Capture4.png',0)
img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,500,
                            param1=30,param2=20,minRadius=50,maxRadius=140)
print(circles)
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)


cv2.imwrite("Detected.png",cimg)




