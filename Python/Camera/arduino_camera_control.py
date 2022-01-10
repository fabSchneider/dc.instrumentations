from serial.serialutil import SerialException
import sys
import os
import camera_capture
import math
import time
import serial

sys.path.append(os.getcwd())

from Polargraph import util
from Polargraph import plotter



# arduino serial settings
port = 'COM5'
baudrate = 115200

# the frequency at which the camera is polled for input (in seconds)
camera_polling_freq = 0.1

# starts sending data to arduino
def run_send(cam, arduino):
    print("Starting to send data from the camera to arduino on port {0} (baudrate: {1})".format(port, baudrate))
    #last_x = math.nan
    #last_y = math.nan
    # start the send loop
    while True:
        x,y = camera_capture.cam_processing(cam)
        x, y = util.clamp_to_unit(x, y)
        plotter.send_xy(arduino, x,y)
        time.sleep(camera_polling_freq)
        
        

       # if(not gamepad.is_running()):
       #     send_xy(arduino, 0, 0)
       #     return "disconnect"
       # if gamepad.X == 1:
       #     send_xy(arduino, 0, 0)
       #     return "stopped"

        #x = gamepad.RightJoystickX
        # invert y to match direction the pen is moving more closely
        #y = gamepad.RightJoystickY
        
        #x, y = clamp_to_unit(x, y)
        
        #if x != last_x or y != last_y :
        #    last_x = x
        #    last_y = y
        #    send_xy(arduino, x, y)

        #time.sleep(camera_polling_freq)

if __name__ == '__main__':

    # create the gamepad listener
    # gpad = gamepad.Gamepad()

    #create camera 
    cam = camera_capture.cam_setup(320, 240)

    try:
        arduino = serial.Serial(port, baudrate, timeout = 0.003)
        response = run_send(cam, arduino)


        #res = run_send(gpad, arduino)   

        #if res == "disconnected":
        #    print("gamepad disconnected")
        #if res == "stopped":
        #    print("sending stopped")
        arduino.close()    
    except SerialException as e:
        print (e)       
   


