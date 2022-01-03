#from array import *
#from typing import Counter 

#vals = array('i',[1,2,3,4,5])

#grid=[[]]
#for row in range[3]:
#    for col in range[3]:
#        grid.append([row, col])

#print (grid)

#grid_2d = [[]]

#for i in range(10):
#    grid_2d[i].append(xPos)
#    grid_2d[i].append(yPos)

#for row in grid_2d:
#    grid_2d[0].append(1)


#print(grid_2d)

#x=0
#def addPosToArray():
#    array.append('1')


#while x < len(vals):
#    addPosToArray()
#    x+=1
#    if vals == 10: 
#        break

#for i in vals:
#    print(i)


import numpy as np
import threading
import time

#numbers = np.arange(9)
#np.append(numbers, 9)

#print(numbers)

#numbers_2d = numbers.reshape(3,3)
#print(numbers_2d)

#print(np.append(numbers_2d, [[100, 30, 2]], axis=0))


#vectorArray = np.array([(0,0)])
#print(vectorArray) 

#vectorArray = np.append(vectorArray, [[xPos,yPos]], axis=0)
#print(vectorArray) 

#rechenarry= np.array([(1, 2),(3, 4)])
#print (rechenarry)

rechenarry= np.array([(0, 0)])


xPos=10
yPos=20



while True:
    rechenarry = np.append(rechenarry, [[xPos,yPos]], axis=0)
    dif = rechenarry[(len(rechenarry)-2)] - rechenarry[(len(rechenarry)-1)]
    print(dif)

    xPos +=2
    yPos +=7
    time.sleep(0.5)
    #data = input()
    #if data =="q":
    #    break

   # differenz = (vectorArray[len(vectorArray-1)])

  #  time.sleep(0.5)

#dif = rechenarry[(len(rechenarry)-2)] - rechenarry[(len(rechenarry)-1)]
#print (dif)


#while True:
#    vectorArray = np.append(vectorArray, [[1,2]], axis=0)
#    print(vectorArray) 
    #data = input()
    #if data =="q":
    #    break

   # differenz = (vectorArray[len(vectorArray-1)])

  #  time.sleep(0.5)
    



