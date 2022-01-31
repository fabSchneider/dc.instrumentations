import keyboard
import time

from Polargraph.gamepad import Gamepad
from Polargraph import task
from Gamepad import gamepad_control

class Plotter:

    def __init__(self, arduino):
        self._arduino = arduino

        # this should go somewhere else
        self.gpad_x_pressed = False
        self.gpad_x_down = False
        self.gpad_y_pressed = False
        self.gpad_y_down = False
        self.gpad_b_pressed = False
        self.gpad_b_down = False
        self.gpad_a_pressed = False
        self.gpad_a_down = False

    # Sends xy command to arduino
    def send_xy(self, x , y):
        self.send("0 {0} {1}\n".format(x, y))
        
    def send_pos(self, x, y):
           self.send("1 {0} {1}\n".format(x, y))

    def send(self, str):
        self._arduino.write(bytes(str, 'ascii'))
        print("[SEND] " + str, end= '')
        # res = self._arduino.readline().decode("utf-8").replace('\n', '')
        # if(len(res) > 0):
        #   print("[ARDUINO] " + res)

    def has_reached_pos(self):
        res = self._arduino.readline().decode("ascii").replace('\r\n', '')
        if len(res) > 0:
            return res == 'r'
        return False

    def read_gpad(self, gpad):
        self.gpad_x_down = False
        self.gpad_y_down = False
        self.gpad_b_down = False
        self.gpad_a_down = False

        if(gpad.X == 1 and not self.gpad_x_pressed):
            self.gpad_x_down = True
        if(gpad.Y == 1 and not self.gpad_y_pressed):
            self.gpad_y_down = True
        if(gpad.B == 1 and not self.gpad_b_pressed):
            self.gpad_b_down = True
        if(gpad.A == 1 and not self.gpad_a_pressed):
            self.gpad_a_down = True

        self.gpad_x_pressed = gpad.X == 1
        self.gpad_y_pressed = gpad.Y == 1
        self.gpad_b_pressed = gpad.B == 1
        self.gpad_a_pressed = gpad.A == 1

    def run(self, programs):
        # create the gamepad listener
        gpad = Gamepad()

        tasks = []

        for program in programs:
            tasks.append(task.PolargraphTask(self, program))

        tasks.append(gamepad_control.GampadControl(gpad, self))

        gpad_task  = len(tasks) - 1
        currTask = gpad_task
        tasks[currTask].start()

        while(not keyboard.is_pressed('esc')):
            self.read_gpad(gpad)

            if len(tasks) > 1 and self.gpad_x_down:
                if(currTask == 0):
                    tasks[currTask].stop()
                    currTask = gpad_task
                    tasks[currTask].start()
                else:
                    tasks[currTask].stop()
                    currTask = 0
                    tasks[currTask].start()
            if len(tasks) > 2 and self.gpad_y_down:
                if(currTask == 1):
                    tasks[currTask].stop()
                    currTask = gpad_task
                    tasks[currTask].start()
                else:
                    tasks[currTask].stop()
                    currTask = 1
                    tasks[currTask].start()
            elif len(tasks) > 3 and self.gpad_b_down:
                if(currTask == 2):
                    tasks[currTask].stop()
                    currTask = gpad_task
                    tasks[currTask].start()
                else:
                    tasks[currTask].stop()
                    currTask = 2
                    tasks[currTask].start()
            elif len(tasks) > 4 and self.gpad_a_down:
                if(currTask == 3):
                    tasks[currTask].stop()
                    currTask = gpad_task
                    tasks[currTask].start()
                else:
                    tasks[currTask].stop()
                    currTask = 3
                    tasks[currTask].start()
                
            time.sleep(0.01)

        tasks[currTask].stop()
        self.send_xy(0, 0)
        print("Program stopped")
