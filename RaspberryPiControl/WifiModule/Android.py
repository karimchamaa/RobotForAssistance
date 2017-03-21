import serial
ser=serial.Serial('/dev/ttyAMA0',9600)

def getWifiData():
    X=0
    Y=0
    C=0

    while(X==0 and Y==0 and C==0):
        ser.write('w')
        X=int(ser.readline())
        Y=int(ser.readline())
        C=int(ser.readline())
    
    return X,Y,C

    
