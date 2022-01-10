# camera capture for line follow drawing machine 

#import libraries 
from tkinter.constants import Y
import cv2
import numpy as np

#variables of old X and Y
old_x = 0.0
old_y= 0.0

#variables of x, y
x = 0
y = 0


#camera setup
def cam_setup(w, h):
    capture = cv2.VideoCapture(1)
    capture.set(3, w)
    capture.set(4, h)
    return capture

#processing camera image 
def cam_processing(capture):
    global old_x
    global old_y
    #initialize capture 
    ret,frame=capture.read()

    #set colors for mask
    low_b = np.uint8([150,80,230])
    high_b = np.uint8([0,0,0])

    # creating Mask 
    mask = cv2.inRange(frame, high_b, low_b)
    #draw contours
    contours,hierarchy = cv2.findContours(mask,1, cv2.CHAIN_APPROX_NONE)

    #check for biggest contour
    if len(contours) >0:
        maxcontour = max(contours, key=cv2.contourArea)
       
        #find and set middlepoint to x and y
        middle = cv2.moments(maxcontour)
        if middle["m00"] !=0:
            x=int(middle["m10"]/middle["m00"])
            y=int(middle["m01"]/middle["m00"])
    
    #calculate difference between old x and y to new x and y 
    xdif= x-old_x
    ydif= y-old_y
    
    # new the x and y to be the old x and y 
    old_x = x
    old_y = y
    print(xdif, ydif)

    return xdif, ydif #, frame, maxcontour, mask 





def cam_show(capture, frame, maxcontour, mask):
    #draw line from old point to new point 
    line = cv2.arrowedLine(frame, (old_x ,old_y), (x, y), (255,255,255), 5)

    #draw circle on old and new point
    cv2.circle(frame,(old_x,old_x),5,(255,255,255), -2)
    cv2.circle(frame,(x,y),5,(0,0,255), -1)
    
    #create contour of detected 
    cv2.drawContours(frame,maxcontour, -1,(255,0,0),1)
    
    #show camera
    cv2.imshow("Camerafeed", frame)
    cv2.imshow("Mask", mask)
    
    #exit if ESC is pressed
    c = cv2.waitKey(1)
    if c == 27:
        capture.release()
        cv2.destroyAllWindows()


