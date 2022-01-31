import serial
from serial.serialutil import SerialException

from Polargraph.plotter import Plotter
from Programs.circle import circle
from Programs.random_walk import random_walk

# arduino serial settings
port = 'COM5'
baudrate = 115200

if __name__ == '__main__':   

    try:
        arduino = serial.Serial(port, baudrate, timeout = 0.003)
        plotter = Plotter(arduino= arduino)
        plotter.run([circle, random_walk])
    except SerialException as e:
        print(e)



