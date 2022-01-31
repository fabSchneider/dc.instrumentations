from inputs import keyboard_process
from serial.serialutil import SerialException
import sys
import os
import math
import time
import serial
import threading
import keyboard

sys.path.append(os.getcwd())

from Polargraph import gamepad
from Polargraph import util

# the frequency at which the gamepad is polled for input (in seconds)
gamepad_polling_freq = 0.03

class GampadControl:

    def __init__(self, gpad, plotter, freq = 0.03):
        self._freq = freq
        self._plotter = plotter
        self._gpad = gpad
        self._running = False

    def is_running(self):
        return self._thread.is_alive()

    def start(self):
        if(self._running):
            return
        self._thread = threading.Thread(target=self._run , args=())
        self._thread.daemon = True
        self._running = True
        self._thread .start()

    def stop(self):
        self._running = False
        self._thread.join()
  
    def _run(self):
        last_x = math.nan
        last_y = math.nan
        # start the send loop
        while self._running:
            if(not self._gpad.is_running()):
                self._plotter.send_xy(0, 0)
                return "disconnect"

            x = self._gpad.RightJoystickX
            y = self._gpad.RightJoystickY
            
            x, y = util.clamp_to_unit(x, y)
            
            if x != last_x or y != last_y :
                last_x = x
                last_y = y
                self._plotter.send_xy(x, y)

            time.sleep(self._freq)

