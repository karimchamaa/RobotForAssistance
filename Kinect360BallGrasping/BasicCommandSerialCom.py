import serial
ser=serial.Serial('/dev/ttyACM0',9600)

while True:
    Command=raw_input("Input Command:")
    ser.write(Command)
 
        
        
