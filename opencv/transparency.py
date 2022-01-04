
import cv2

image = cv2.imread('assets/grumpy.jpg',1)
overlay = image.copy()

x, y, w, h = 10, 10, 10, 10  # Rectangle parameters
cv2.rectangle(overlay, (x, y), (x+w, y+h), (0, 200, 0), -1)  # A filled rectangle

alpha = 0.4  # Transparency factor.

# Following line overlays transparent rectangle over the image
image_new = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)