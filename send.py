import serial
import time

ser=serial.Serial("/dev/ttyS1",9600)
ser.baudrate=9600

A=2

ser.write(str(A))

# while True:   
#     ser.write("%d" %x)
#     time.sleep(0.1)