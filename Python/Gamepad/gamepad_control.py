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
from Polargraph import plotter

# arduino serial settings
port = 'COM5'
baudrate = 115200

# the frequency at which the gamepad is polled for input (in seconds)
gamepad_polling_freq = 0.03

class GampadControl:

    def __init__(self, gpad, arduino, freq = 0.03):
        self._freq = freq
        self._arduino = arduino
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
        print("Starting to send data from the gamepad to arduino on port {0} (baudrate: {1})".format(port, baudrate))
        last_x = math.nan
        last_y = math.nan
        # start the send loop
        while self._running:
            if(not self._gpad.is_running()):
                plotter.send_xy(self._arduino, 0, 0)
                return "disconnect"
            # if gpad.X == 1:
            #     plotter.send_xy(arduino, 0, 0)
            #     return "stopped"

            x = self._gpad.RightJoystickX
            # invert y to match direction the pen is moving more closely
            y = self._gpad.RightJoystickY
            
            x, y = util.clamp_to_unit(x, y)
            
            if x != last_x or y != last_y :
                last_x = x
                last_y = y
                plotter.send_xy(self._arduino, x, y)

            time.sleep(self._freq)
        print("Stop thread")

if __name__ == '__main__':

    # create the gamepad listener
    gpad = gamepad.Gamepad()

    try:
        arduino = serial.Serial(port, baudrate, timeout = 0.003)
        gpad_control = GampadControl(gpad, arduino)

        gpad_control.start()

        while(not keyboard.is_pressed('esc')):  
            if(gpad.Y == 1):
                if(gpad_control.is_running()):
                    gpad_control.stop()
                    print("stopped gamepad control")
                else:
                    gpad_control.start()
                    print("start gamepad control")
                
            time.sleep(0.1)

        gpad_control.stop()
        print("Program stopped")

        arduino.close()    
    except SerialException as e:
        print (e)       
   


