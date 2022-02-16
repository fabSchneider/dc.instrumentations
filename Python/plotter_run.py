import serial
from serial.serialutil import SerialException

from Polargraph.plotter import Plotter
from Programs.circle import circle
from Programs.random_walk import random_walk_sequence
from Programs.home import home
from Programs.random_pos import random_brush
from Programs.camera_feed import camera_feed_circles
from Programs.cover import cover, back_forth
import time_utils
import time

# arduino serial settings
# port = 'COM5'
port = '/dev/ttyACM0'
baudrate = 115200

if __name__ == '__main__':   

    try:
        arduino = serial.Serial(port, baudrate, timeout = 0.003)
        plotter = Plotter(arduino)
        plotter.run(random_walk_sequence, run_time = time_utils.hour_to_sec(8))
    except SerialException as e:
        print(e)
    else:
        arduino.close()
