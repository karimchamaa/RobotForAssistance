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
import math
import array
ser=serial.Serial('/dev/ttyAMA0',9600)
ser.write('a')#AttachServos 

def grab(Color):
        #Request Y-axis,Camera 
        ser.write('1')
        time.sleep(1)
        ap = argparse.ArgumentParser()
        ap.add_argument("-v",
                help="path to the (optional) video file")
        ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
        args = vars(ap.parse_args())

        # Color Selection - Blue :1 Yellow:2
        if(Color==2):
                #Yellow Colour
                yellowLower = (25, 110, 110)
                yellowUpper = (30, 255, 255)
        if(Color==1):
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
                blurred = cv2.GaussianBlur(frame, (11, 11), 0)
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, yellowLower, yellowUpper)
                mask = cv2.erode(mask, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)
                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)[-2]
                center = None
                if len(cnts) > 0:
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
                                break
                        if radius > 10:
                                cv2.circle(frame, (int(x), int(y)), int(radius),
                                        (0, 255, 255), 2)
                                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                pts.appendleft(center)
                #cv2.imshow("Frame", frame)
                rawCapture.truncate(0) 
                key = cv2.waitKey(1) & 0xFF
                
        yd=input("Y:")
        yd=float(yd)

        #Request X-axis,Ultrasonic Sensor 
        ser.write('x')
        xd=int(ser.readline())*0.1
        print "xd:",xd

        #Define Manipulator Parameter
        OrientationArray=[0,math.pi/2,math.pi/4,math.pi/6,-math.pi/2,-math.pi/4,-math.pi/6,-math.pi,0.1,0.7]
        l1=14.5
        l2=18.5
        l3=18
        flag=0
        col=0

        #Find Angles and Corresponding Orientation
        while flag==0:
            Orientation=OrientationArray[col]
            x=xd-(l3*math.cos(Orientation))
            y=yd-(l3*math.sin(Orientation))
            D=((math.pow(x,2))+(math.pow(y,2))-(math.pow(l1,2))-(math.pow(l2,2)))/(2*l1*l2)
            if(isinstance(D, float) & (pow(D,2)<=1)):
                Angle2=math.atan2(-math.sqrt(1-(math.pow(D,2))),D)
                Angle1=math.atan2(y,x)-math.atan2(l2*math.sin(Angle2),l1+(l2*math.cos(Angle2)))
                Angle3=Orientation-Angle1-Angle2
                if( (Angle1>math.pi) | (Angle1<0) | (Angle2>0) | (Angle2<-math.pi) | (Angle3>0) | (Angle3<-math.pi) ):
                    flag=0
                else:
                    flag=1
            col=col+1


        #Check Values using Forward Kinematics
        dx=18*math.cos(Angle1 + Angle2 + Angle3) + (37*math.cos(Angle1 + Angle2))/2 + (29*math.cos(Angle1))/2
        dy=18*math.sin(Angle1 + Angle2 + Angle3) + (37*math.sin(Angle1 + Angle2))/2 + (29*math.sin(Angle1))/2

        #Angles to pulses
        Pulse1=int(round(((185.0/18)*math.degrees(Angle1))+550))
        Pulse2=int(round(((185.0/18)*abs(math.degrees(Angle2)))+550))
        Pulse3=int(round(((185.0/18)*abs(math.degrees(Angle3)))+550))

        #Printing Values
        print "Angle1=",math.degrees(Angle1)
        print "Angle2=",math.degrees(Angle2)
        print "Angle3=",math.degrees(Angle3)
        print "X=",dx
        print "Y=",dy
        print "Orientation=",math.degrees(Orientation)
        print "Pulse1=",Pulse1
        print "Pulse2=",Pulse2
        print "Pulse3=",Pulse3

        #Should I Send Codes
        Send=input("Send:")

        #Send Them Serially
        ser.write('5')#Open Arm
        ser.write('1')
        time.sleep(0.2)
        Pulse1=str(Pulse1+1000)
        Pulse2=str(Pulse2+1000)
        Pulse3=str(Pulse3+1000)
        ser.write('2')
        ser.write(Pulse1)
        ser.write('3')
        ser.write(Pulse2)
        ser.write('4')
        ser.write(Pulse3)
        ser.write('s')
        ser.write('5') #Close Arm
        ser.write('0')


        #Return Arm Back to Initial Position
        Send=input("Send Back:")
        ser.write('2')
        ser.write('2783')
        ser.write('3')
        ser.write('2269')
        ser.write('4')
        ser.write('2783')
        ser.write('s')
        ser.write('d')#Detach Servos 









