#Pyhton Code für opencv to detect direction movement

#Libraries importieren 
import cv2
import numpy as np
import time

from tkinter import *

#arduino verbindung
import pyfirmata
#arduino = pyfirmata.Arduino('COM3')

#Videocapture initialisieren 
capture = cv2.VideoCapture(1)
capture.set(3, 630)
capture.set(4, 480)

#Positionarray erstellen
posArray= np.array([(0, 0)])

#setup von arrow drawing
#canvas = Tk()
#canvas.title("Arrow Test")
#canvas.geometry("700x700")
#my_can = Canvas(canvas, width=600, height=600, bg="gray")
#my_can.pack(pady=50) 


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
           # print("CenterX: "+ str(cx)+" CenterY: "+ str(cy))
            
            #aktuellen wert ins array schreiben und mit dem unteren vergleichen
            time.sleep(0.5)


            posArray = np.append(posArray, [[cx,cy]], axis=0)
            dif = posArray[(len(posArray)-2)] - posArray[(len(posArray)-1)]
            aktuell = posArray[(len(posArray)-1)]
            alt = posArray[(len(posArray)-2)]
            #print(dif)
           # print(dif[0])
            #print(dif[1])
            xAlt = alt[0]
            yAlt = alt[1]
            x = aktuell[0]
            y = aktuell[1]
            print("alt")
            print(xAlt)
            print(yAlt)
            print("neu")
            print(x)
            print(y)    

            mappeddif = np.interp(dif, [-100, 100],[-1, 1])
            #print(mappeddif) 
            
            #my_can.create_line(cx, cy, x, y, fill="black", width=5, arrow="last")
            
            line = cv2.arrowedLine(frame, (xAlt ,yAlt), (x, y), (255,255,255), 10)
            #draw circle
            cv2.circle(frame,(xAlt,yAlt),5,(255,255,255), -2)
            
            

            

            cv2.circle(frame,(x,y),5,(0,0,255), -1)
            """
            #X Achse 
            if cx >=365:
                print("Left")
               #alle anderen ausschalten und richtigen einschalten
                arduino.digital[10].write(0)
                arduino.digital[9].write(0)
                arduino.digital[6].write(1)
                arduino.digital[3].write(0)

            if cx <365 and cx>265:
                print("X ok")

            if cx <=265:
                print("Right")
               #alle anderen ausschalten und richtigen einschalten
                arduino.digital[10].write(0)
                arduino.digital[9].write(1)
                arduino.digital[6].write(0)
                arduino.digital[3].write(0)

            #Y Achse
            if cy >=280:
                print("Up")
               #alle anderen ausschalten und richtigen einschalten
                arduino.digital[10].write(0)
                arduino.digital[9].write(0)
                arduino.digital[6].write(0)
                arduino.digital[3].write(1)

            if cy <280 and cx>200:
                print("Y ok")

            if cy <=200:
                print("Up")
                #alle anderen ausschalten und richtigen einschalten
                arduino.digital[10].write(1)
                arduino.digital[9].write(0)
                arduino.digital[6].write(0)
                arduino.digital[3].write(0)

                """

            


        cv2.drawContours(frame,maxcontour, -1,(255,0,0),1)



    #show camera
    cv2.imshow("Camerafeed", line)
    cv2.imshow("Mask", mask)


    #exit if ESC is pressed
    c = cv2.waitKey(1)
    if c == 27:
        break
#canvas.mainloop()
capture.release()
cv2.destroyAllWindows()

