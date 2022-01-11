from serial.serialutil import SerialException
import sys
import os
import keyboard
import time
import serial
import math
import random

sys.path.append(os.getcwd())

from Polargraph import util
from Polargraph import plotter
from Polargraph import gamepad
from Polargraph import task
from Gamepad import gamepad_control

# arduino serial settings
port = 'COM5'
baudrate = 115200

gpad_y_pressed = False
gpad_y_down = False
gpad_b_pressed = False
gpad_b_down = False

def read_gpad(gpad):
    global gpad_y_pressed 
    global gpad_y_down 
    global gpad_b_pressed 
    global gpad_b_down 

    gpad_y_down = False
    gpad_b_down = False
    if(gpad.Y == 1 and not gpad_y_pressed):
        gpad_y_down = True
    if(gpad.B == 1 and not gpad_b_pressed):
        gpad_b_down = True

    gpad_y_pressed = gpad.Y == 1
    gpad_b_pressed = gpad.B == 1

def run_circle(task):
    print("Starting circle")
    pos = 0.0

    while task._running:
        pos += 0.03
        plotter.send_xy(task._arduino, math.sin(pos), math.cos(pos))
        time.sleep(0.03)

    # send stop
    plotter.send_xy(task._arduino, 0, 0)
    print("Stopped circle")

def run_random(task):
    print("Starting random walk")
    dir = random.uniform(-math.pi, math.pi)
    while task._running:
        dir += random.uniform(-math.pi * 0.5, math.pi * 0.5)
        x = math.cos(dir)
        y = math.sin(dir)
        plotter.send_xy(task._arduino, x, y)
        time.sleep(0.5)

    # send stop
    plotter.send_xy(task._arduino, 0, 0)
    print("Stopped random walks")

def main():
    # create the gamepad listener
    gpad = gamepad.Gamepad()

    try:
        arduino = serial.Serial(port, baudrate, timeout = 0.003)

        circleTask = task.PolargraphTask(arduino, run_circle)
        randomTask = task.PolargraphTask(arduino, run_random)


        gpad_control = gamepad_control.GampadControl(gpad, arduino)
        gpad_control.start()

        currTask = gpad_control

        while(not keyboard.is_pressed('esc')):
            read_gpad(gpad)

            if(gpad_y_down):
                if(currTask == circleTask):
                    circleTask.stop()
                    currTask = gpad_control
                    currTask.start()
                else:
                    currTask.stop()
                    currTask = circleTask
                    currTask.start()
            elif(gpad_b_down):
                if(currTask == randomTask):
                    randomTask.stop()
                    currTask = gpad_control
                    currTask.start()
                else:
                    currTask.stop()
                    currTask = randomTask
                    currTask.start()
                
            time.sleep(0.01)

        currTask.stop()
        plotter.send_xy(arduino, 0, 0)
        arduino.close()    
        print("Program stopped")

    except SerialException as e:
        print (e)   

if __name__ == '__main__':   
   main()
 


