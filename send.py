import serial
import time
x=1
ser=serial.Serial("/dev/ttyS1",9600)
ser.baudrate=9600


while True:   
    ser.write("%d" %x)
    time.sleep(0.1)