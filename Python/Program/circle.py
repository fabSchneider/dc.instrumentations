from serial.serialutil import SerialException
import sys
import os
import keyboard
import time
import serial
import math
import random

sys.path.append(os.getcwd())

from Polargraph import plotter

# arduino serial settings
port = 'COM5'
baudrate = 115200

# the frequency at which new directions are generated
freq = 0.1
changeRate = 0.03

# starts sending data to arduino
def do_circle(arduino, freq, changeRate):
    print("Starting to send data to arduino on port {0} (baudrate: {1})".format(port, baudrate))
    pos = 0.0

    # start the send loop
    while not keyboard.is_pressed('esc'):
        pos = (pos + changeRate) % 1.0
        plotter.send_xy(arduino, math.sin(pos), math.cos(pos))
        time.sleep(freq)

    # send stop
    plotter.send_xy(arduino, 0, 0)
    print("stopped")

if __name__ == '__main__':

    try:
        arduino = serial.Serial(port, baudrate, timeout = 0.003)
        do_circle(arduino, freq, changeRate)   
        arduino.close()    
    except SerialException as e:
        print (e)       
   


