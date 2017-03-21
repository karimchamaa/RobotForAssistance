import serial
ser=serial.Serial('/dev/ttyAMA0',9600)

while True:
    Command=raw_input("Input Command:")
    ser.write(Command)
    if(Command=='x'):
        response=ser.readline()
        distance=int(response)*0.1
        print distance
    if(Command=='o'):
        resp=ser.readline()
        dist=int(resp)
        print dist
    if(Command=='f'):
        response=ser.readline()
        ser.write('g')

        
        
