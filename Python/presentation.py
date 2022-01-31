import serial
from serial.serialutil import SerialException

from Polargraph.plotter import Plotter
from Programs.circle import circle
from Programs.random_walk import random_walk
from Programs.home import home
from Programs.random_pos import random_brush
from Programs.camera_feed import camera_feed

# arduino serial settings
port = 'COM5'
baudrate = 115200

if __name__ == '__main__':   

    try:
        arduino = serial.Serial(port, baudrate, timeout = 0.003)
        plotter = Plotter(arduino)
        plotter.run([home, camera_feed, random_walk, random_brush])
    except SerialException as e:
        print(e)

    arduino.close()

