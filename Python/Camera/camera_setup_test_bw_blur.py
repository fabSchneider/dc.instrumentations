#Pyhton Code für opencv to detect direction movement

#Libraries importieren 
import cv2
import numpy as np
import time

from tkinter import *

radius = 151 #must be an odd number, or else GaussianBlur will fail
circleColor = (255, 255, 255)
circleThickness = 15

#Videocapture initialisieren 
capture = cv2.VideoCapture(1)
capture.set(3, 360)
capture.set(4, 240)

#Positionarray erstellen
posArray= np.array([(0, 0)])

while True:
    ret,frame=capture.read()
    image = frame.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (radius, radius), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    cv2.circle(gray, minLoc, 10, circleColor, circleThickness)
    print(minLoc)
    #image = frame.copy()

    cv2.imshow("Robust", gray)
    #exit if ESC is pressed
    c = cv2.waitKey(1)
    if c == 27:
        break
#canvas.mainloop()
capture.release()
cv2.destroyAllWindows()

