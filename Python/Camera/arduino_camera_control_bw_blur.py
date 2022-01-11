from tkinter.constants import NONE
from serial.serialutil import SerialException
import sys
import os
#from Camera.camera_capture import cam_show
import camera_capture_bw_blur
import keyboard
import time
import serial
import cv2


sys.path.append(os.getcwd())

from Polargraph import util
from Polargraph import plotter



# arduino serial settings
port = 'COM5'
baudrate = 115200

# the frequency at which the camera is polled for input (in seconds)
camera_polling_freq = 0.03
factor = 0.0001

# starts sending data to arduino
def run_send(cam, arduino):
    print("Starting to send data from the camera to arduino on port {0} (baudrate: {1})".format(port, baudrate))
    # start the send loop
    while not keyboard.is_pressed('esc'): 
        x, y, f = camera_capture_bw_blur.cam_processing(cam)
        x = x * factor
        y = y * factor
        x, y = util.clamp_to_unit(x, y)
        
        x=-x
        y=-y
        print(x, y)
        plotter.send_xy(arduino, x,y)
        time.sleep(camera_polling_freq)

        camera_capture_bw_blur.cam_show(cam, f)
        #if(not c ==NONE):
        #    camera_capture.cam_mask_show(cam, f, c, m)
        #camera_capture.cam_show(cam, f, c, m)
        
    plotter.send_xy(arduino, 0, 0)
    cv2.destroyAllWindows()
    cam.release() 




if __name__ == '__main__':

    # create the gamepad listener
    # gpad = gamepad.Gamepad()

    #create camera 
    cam = camera_capture_bw_blur.cam_setup(320, 240)

    try:
        arduino = serial.Serial(port, baudrate, timeout = 0.003)
        response = run_send(cam, arduino)
        arduino.close()    
    except SerialException as e:
        print (e)       
   


