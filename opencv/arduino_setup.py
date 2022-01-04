# Importing Libraries
import serial
#import time

#arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
#def write_read(x):
#    arduino.write(bytes(x, 'utf-8'))
#    time.sleep(0.05)
#    data = arduino.readline()
#    return data
#while True:
#    num = input("Enter a number: ") # Taking input from user
#    value = write_read(num)
#    print(value) # printing the value


import time
import pyfirmata

arduino = pyfirmata.Arduino('COM3')

while True:
    arduino.digital[10].write(1)
    time.sleep(1)
    arduino.digital[10].write(0)
    time.sleep(1)

    arduino.digital[9].write(1)
    time.sleep(1)
    arduino.digital[9].write(0)
    time.sleep(1)

    arduino.digital[6].write(1)
    time.sleep(1)
    arduino.digital[6].write(0)
    time.sleep(1)

    arduino.digital[3].write(1)
    time.sleep(1)
    arduino.digital[3].write(0)
    time.sleep(1)