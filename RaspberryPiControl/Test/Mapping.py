import math
import time
import numpy
from PIL import Image
import serial
import Astar
import Map
ser=serial.Serial('/dev/ttyAMA0',9600)

def drive(xA,yA,xB,yB,myOrientation):
    dirs = 8 
    dx = [1, 1, 0, -1, -1, -1, 0, 1]
    dy = [0, 1, 1, 1, 0, -1, -1, -1]

    # Main Code to be edited

    # Generate  Map  
    [n,m,the_map]=Map.Generate()

    #Find Shortest Path 
    route = Astar.pathFind(the_map, n, m, dirs, dx, dy, xA, yA, xB, yB)

    #Print Route in S F O Format 
    [RowMapped,ColMapped]=Map.Print(dx,dy,route,yA,xA,yB,xB,n,m,the_map)

   
        
    # Genereate Driving Command from mapped data and Send Command Serially
    for i in range(1,len(RowMapped)):
        if(RowMapped[i]==RowMapped[i-1] and ColMapped[i]==ColMapped[i-1]+1):
            TurningRate=0-myOrientation
            myOrientation=0
            EncoderDistance=3
        if(RowMapped[i]==RowMapped[i-1]-1 and ColMapped[i]==ColMapped[i-1]):
            TurningRate=-90-myOrientation
            myOrientation=-90
            EncoderDistance=3
        if(RowMapped[i]==RowMapped[i-1]-1 and ColMapped[i]==ColMapped[i-1]+1):
            TurningRate=-45-myOrientation
            myOrientation=-45
            EncoderDistance=4
        if(RowMapped[i]==RowMapped[i-1]+1 and ColMapped[i]==ColMapped[i-1]):
            TurningRate=90-myOrientation
            myOrientation=90
            EncoderDistance=3
        if(RowMapped[i]==RowMapped[i-1]+1 and ColMapped[i]==ColMapped[i-1]+1):
            TurningRate=45-myOrientation
            myOrientation=45
            EncoderDistance=4
        if(RowMapped[i]==RowMapped[i-1] and ColMapped[i]==ColMapped[i-1]-1):
            TurningRate=-180-myOrientation
            myOrientation=-180
            EncoderDistance=3
        if(RowMapped[i]==RowMapped[i-1]-1 and ColMapped[i]==ColMapped[i-1]-1):
            TurningRate=-135-myOrientation
            myOrientation=-135
            EncoderDistance=4
        if(RowMapped[i]==RowMapped[i-1]+1 and ColMapped[i]==ColMapped[i-1]-1):
            TurningRate=135-myOrientation
            myOrientation=135
            EncoderDistance=4
        if(TurningRate !=0):
            print "Turn by:", TurningRate
        if(TurningRate==45):
            ser.write('r')
            ser.readline()
            #ser.write('g')
            time.sleep(0.1)
        if(TurningRate==90):
            ser.write('e')
            ser.readline()
            #ser.write('g')
            time.sleep(0.1)
        if(TurningRate==-45):
            ser.write('l')
            ser.readline()
            #ser.write('g')
            time.sleep(0.1)
        if(TurningRate==-90 or TurningRate==270):
            ser.write('k')
            ser.readline()
            #ser.write('g')
            time.sleep(0.1)
        if(abs(TurningRate)==180):
            ser.write('t')
            ser.readline()
            #ser.write('g')
            time.sleep(0.1)
        #Change Encoder Distance
        if(EncoderDistance==3):
            print "Distance 330"
            ser.write('v')
            ser.write('3')
        else:
            print "Distance 469"
            ser.write('v')
            ser.write('4')
            
        print "Forward"      
        ser.write('f')
        ser.readline()
        #ser.write('g')
        time.sleep(0.1)
        
        
    print "Stop"
    ser.write('g')
  














