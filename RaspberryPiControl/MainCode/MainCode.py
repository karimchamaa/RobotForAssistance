import Android
import Mapping
import Manipulator
import time
xStart=6
yStart=7
xB=0
yB=0
myOrientation=-90

while True:
    #Wifi 
    [xB,yB,C]=Android.getWifiData(xB,yB)

    #Mapping 
    myOrientation=Mapping.drive(xStart,yStart,yB,xB,myOrientation)
    time.sleep(30)

    #Manipulator
    #Manipulator.grab(C) #2-Yelow Ball,1-Blue Ball

    #Mapping 
    myOrientation=Mapping.drive(yB,xB,xStart,yStart,myOrientation)






