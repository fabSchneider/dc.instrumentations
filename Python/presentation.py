import serial
from serial.serialutil import SerialException

from Polargraph.plotter import Plotter
from Programs.circle import circle
from Programs.random_walk import random_walk
from Programs.home import home
from Programs.random_pos import random_brush
from Programs.camera_feed import camera_feed
import time_utils

# arduino serial settings
# port = 'COM5'
port = '/dev/ttyACM0'
baudrate = 115200

if __name__ == '__main__':   

    try:
        arduino = serial.Serial(port, baudrate, timeout = 0.003)
        plotter = Plotter(arduino)
        plotter.run([home, camera_feed, random_walk, random_brush], run_time = time_utils.hour_to_sec(3))
    except SerialException as e:
        print(e)

    arduino.close()

