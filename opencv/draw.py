import cv2 as cv
import numpy as np

#create a new blank image with 500 x 500 
blank = np.zeros((500,500,3), dtype="uint8")
#cv.imshow("Blank", blank)

# color the whole image 
#blank[:] = 0,255,0
#cv.imshow("Green", blank)

#color a spesific space on the image 
#blank[200:300, 300:400]=0,0,255

# rectangle with outline
#cv.rectangle(blank, (0,0), (250,250),(255,255,0),thickness=2)

#fill rect

cv.rectangle(blank, (0,0), (250,250),(255,255,0),thickness=-1)
#cv.putText(blank, "TEXT", (255,255), cv.FONT_HERSHEY_TRIPLEX, 1.0, (0,0,255), 2)

cv.imshow("Small Rectangle", blank)

#img = cv.imread("assets/grumpy.jpg")
#cv.imshow("headline", img)

cv.waitKey(0)