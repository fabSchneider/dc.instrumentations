import time
import math

def circle(task):
    print("Starting circle")
    pos = 0.0

    while task._running:
        pos += 0.03
        task.plotter.send_xy(math.sin(pos), math.cos(pos))
        time.sleep(0.03)

    # send stop
    task.plotter.send_xy(0, 0)
    print("Stopped circle")