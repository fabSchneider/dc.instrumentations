import cv2

img = cv2.imread("assets/grumpy.jpg", 1)

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows 