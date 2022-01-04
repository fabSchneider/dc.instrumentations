import cv2
import numpy as np

capture = cv2.VideoCapture(1)
capture.set(3, 160)
capture.set(4, 120)

while True:
    ret,frame=capture.read()

    # creating filter for mask 
    low_b = np.uint8([30,30,30])
    high_b = np.uint8([0,0,0])

    # creating Mask 
    mask = cv2.inRange(frame, high_b, low_b)
    #draw contours
    contours,hierarchy = cv2.findContours(mask,1, cv2.CHAIN_APPROX_NONE)
    

    #only take the biggest black contour available 
    if len(contours) >0:
        maxcontour = max(contours, key=cv2.contourArea)
       
        #find and draw middlepoint 
        middle = cv2.moments(maxcontour)
        if middle["m00"] !=0:
            cx=int(middle["m10"]/middle["m00"])
            cy=int(middle["m01"]/middle["m00"])

            #print middlepoint + directions in console 
            print("CenterX: "+ str(cx)+" CenterY: "+ str(cy))

            #X Achse 
            if cx >=120:
                print("Left")
            if cx <120 and cx>40:
                print("X ok")
            if cx <=40:
                print("Right")
            #Y Achse
            if cy >=120:
                print("Down")
            if cy <120 and cx>40:
                print("Y ok")
            if cx <=40:
                print("Up")

            #draw circle
            cv2.circle(frame,(cx,cy),5,(255,255,255), -1)


        cv2.drawContours(frame,maxcontour, -1,(255,0,0),1)



    #show camera
    cv2.imshow("Camerafeed", frame)
    cv2.imshow("Mask", mask)

    #exit if ESC is pressed
    c = cv2.waitKey(1)
    if c == 27:
        break

capture.release()
cv2.destroyAllWindows()

