import camera_capture
import time

cam = camera_capture.cam_setup(320, 240)

i=0
while i<10: 
    cam_output = camera_capture.cam_processing(cam)
   # send(arduino, cam_output[0], cam_output[1])
    time.sleep(0.2)
    i+=1

