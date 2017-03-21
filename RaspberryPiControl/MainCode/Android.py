import serial
ser=serial.Serial('/dev/ttyAMA0',9600)

def getWifiData(xB,yB):
    
    while True:
        ser.write('w')
        X=int(ser.readline())
        Y=int(ser.readline())
        C=int(ser.readline())
        if (X==xB and Y==yB):
            KLM=1
        else:
            break
    return X,Y,C
