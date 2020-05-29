import serial
import time

ser=serial.Serial("/dev/ttyS1",9600)
ser.baudrate=9600

while True:
    read_ser=ser.readline()
    #read_ser='1,2'
    values = read_ser.split(',')
    
    print(values[0])
    print(values[1])
    