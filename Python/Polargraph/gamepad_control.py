import time
import math
from Polargraph.gamepad import Gamepad
from Polargraph import util

def gamepad_control(task):
    print("Starting gamepad control")
    last_x = math.nan
    last_y = math.nan

    gpad = Gamepad()

    # start the send loop
    while task._running and  gpad.is_running():
        x = gpad.RightJoystickX
        y = gpad.RightJoystickY
        
        x, y = util.clamp_to_unit(x, y)
        
        if x != last_x or y != last_y :
            last_x = x
            last_y = y
            task.plotter.send_xy(x, y)

        time.sleep(0.03)

    # send stop
    task.plotter.send_xy(0, 0)
    print("Stopped gamepad control")