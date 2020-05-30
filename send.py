import serial
import time

ser=serial.Serial("/dev/ttyS1",9600)
ser.baudrate=9600
A = None
c=int(A)


x=1
while True:   
    ser.write("%d" %x)
    time.sleep(0.1)