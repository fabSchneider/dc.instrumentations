# camera capture for line follow drawing machine 

#import libraries 
from tkinter.constants import NONE, Y
import cv2
import numpy as np

#variables for gaussian and circle 
radius = 111 #must be an odd number, or else GaussianBlur will fail
circleColor = (255, 255, 255)
circleThickness = 15

#camera setup
def cam_setup(w, h):
    capture = cv2.VideoCapture(1)
    capture.set(3, w)
    capture.set(4, h)
    return capture

#processing camera image 
def cam_processing(capture):

    #initialize capture 
    ret,frame=capture.read()
    image = frame.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (radius, radius), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    cv2.circle(gray, minLoc, 10, circleColor, circleThickness)
    x,y = minLoc

    return x, y, gray

    
   

def cam_show(capture, frame):
    cv2.imshow("Camerafeed", frame)
     #exit if ESC is pressed
    c = cv2.waitKey(1)
    if c == 27:
        capture.release()
        cv2.destroyAllWindows()