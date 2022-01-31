import keyboard
import time

from Polargraph.gamepad import Gamepad
from Polargraph import task
from Gamepad import gamepad_control

class Plotter:

    def __init__(self, arduino):
        self._arduino = arduino

        # this should go somewhere else
        self.gpad_y_pressed = False
        self.gpad_y_down = False
        self.gpad_b_pressed = False
        self.gpad_b_down = False

    # Sends xy command to arduino
    def send_xy(self, x , y):
        sendStr = "{0} {1}\n".format(x, y)
        self._arduino.write(bytes(sendStr, 'utf-8'))
        print("[SEND] " + sendStr, end= '')
        res = self._arduino.readline().decode("utf-8").replace('\n', '')
        if(len(res) > 0):
            print("[ARDUINO] " + res)

    def read_gpad(self, gpad):
        self.gpad_y_down = False
        self.gpad_b_down = False
        if(gpad.Y == 1 and not self.gpad_y_pressed):
            self.gpad_y_down = True
        if(gpad.B == 1 and not self.gpad_b_pressed):
            self.gpad_b_down = True

        self.gpad_y_pressed = gpad.Y == 1
        self.gpad_b_pressed = gpad.B == 1

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

            if len(tasks) > 1 and self.gpad_y_down:
                if(currTask == 0):
                    tasks[currTask].stop()
                    currTask = gpad_task
                    tasks[currTask].start()
                else:
                    tasks[currTask].stop()
                    currTask = 0
                    tasks[currTask].start()
            elif len(tasks) > 2 and self.gpad_b_down:
                if(currTask == 1):
                    tasks[currTask].stop()
                    currTask = gpad_task
                    tasks[currTask].start()
                else:
                    tasks[currTask].stop()
                    currTask = 1
                    tasks[currTask].start()
                
            time.sleep(0.01)

        tasks[currTask].stop()
        self.send_xy(0, 0)
        print("Program stopped")
