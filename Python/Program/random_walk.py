from serial.serialutil import SerialException
import sys
import os
import keyboard
import time
import serial
import random

sys.path.append(os.getcwd())

from Polargraph import util
from Polargraph import plotter

# arduino serial settings
port = 'COM5'
baudrate = 115200

# the frequency at which new directions are generated
freq = 1.5

# starts sending data to arduino
def do_random_walk(seed, arduino):
    print("Starting to send data to arduino on port {0} (baudrate: {1})".format(port, baudrate))

    random.seed(seed)
    # start the send loop
    while not keyboard.is_pressed('esc'):
        send_random(arduino)    
        time.sleep(freq)

    # send stop
    plotter.send_xy(arduino, 0, 0)
    print("stopped")

def send_random(arduino):
    x = random.uniform(-1.0, 1.0)
    y = random.uniform(-1.0, 1.0)
    
    x, y = util.normalize(x, y)
    plotter.send_xy(arduino, x, y)

if __name__ == '__main__':


    try:
        arduino = serial.Serial(port, baudrate, timeout = 0.003)
        do_random_walk(5323, arduino)   
        arduino.close()    
    except SerialException as e:
        print (e)       
   


