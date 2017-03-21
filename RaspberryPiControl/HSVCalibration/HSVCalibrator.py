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



#yellowLower = (20, 100, 100)
#yellowUpper = (30, 255, 255)

print "20,100,100"
print "30,255,255"

Low1=input("Low1:")
Low2=input("Low2:")
Low3=input("Low3:")
Up1=input("Up1:")
Up2=input("Up2:")
Up3=input("Up3:")
BlueLower = (Low1, Low2, Low3)
BlueUpper = (Up1, Up2, Up3)
Choice=input("Image Number:")
if Choice==1:
    img = cv2.imread('Capture1.png',1)
if Choice==2:
    img = cv2.imread('Capture2.png',1)
if Choice==3:
    img = cv2.imread('Capture4.png',1)
blurred = cv2.GaussianBlur(img, (11, 11), 0)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, BlueLower, BlueUpper)
cv2.imwrite("Masked2.png",mask)
mask = cv2.erode(mask, None, iterations=2)
mask = cv2.dilate(mask, None, iterations=2)
cv2.imwrite("Eroded2.png",mask)


#Calibrated Values       
#BLUE COLOR RANGE:
#LOW: 100,50,50
#Up:130,255,255

# Yellow Range
#Low:25,110,110
#HIGH:30,255,255

#Old Values
#Yellow Colour
#yellowLower = (20, 100, 100)
#yellowUpper = (30, 255, 255)
#Blue Colour 
#yellowLower = (110, 50, 50)
#yellowUpper = (130, 255, 255)







