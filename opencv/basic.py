import cv2 as cv


img = cv.imread("assets/grumpy.jpg", 1)
cv.imshow("Cat", img)


#convert to grayscale 
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow("Gray", gray)

#Blur image 
blur = cv.GaussianBlur(img,(7,7), cv.BORDER_DEFAULT)
cv.imshow("Blure", blur)

#Edge cascade 
cany =cv.Canny(blur, 125,175)
cv.imshow("Canny Edges", cany)

#Dilatte image 
dilated= cv.dilate(cany, (7,7), iterations=3)
cv.imshow("Dilated", dilated)

#resizing 
resized = cv.resize(img, (500,500), interpolation=cv.INTER_CUBIC)
cv.imshow("Resized", resized)
#cropping also possible 
 


cv.waitKey(0)