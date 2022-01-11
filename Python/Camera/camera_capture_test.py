import camera_capture
import time
import os
import sys
import keyboard

sys.path.append(os.getcwd())

from Polargraph import util
from Polargraph import plotter

factor = 0.001

cam = camera_capture.cam_setup(320, 240)

while not keyboard.is_pressed('esc'): 
    x, y = camera_capture.cam_processing(cam)
    x = x * factor
    y = y * factor

    x, y = util.clamp_to_unit(x, y)

    print(x,y)
    #cam_output = camera_capture.cam_processing(cam_output[2], cam_output[3], cam_output[4])
   # send(arduino, cam_output[0], cam_output[1])
    time.sleep(0.2)

print('Stopping')
cam.release()

