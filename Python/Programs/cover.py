import time
import math

LIMIT_MIN_X = -450
LIMIT_MAX_X = 450
LIMIT_MIN_Y = -700
LIMIT_MAX_Y = 700

LIMIT_MIN_X = -100
LIMIT_MAX_X = 100
LIMIT_MIN_Y = -200
LIMIT_MAX_Y = 200

pts = [(LIMIT_MIN_X, LIMIT_MIN_Y), 
       (LIMIT_MAX_X, LIMIT_MIN_Y),
       (LIMIT_MAX_X, LIMIT_MAX_Y),
       (LIMIT_MIN_X, LIMIT_MAX_Y),
       (LIMIT_MIN_X, LIMIT_MIN_Y)]

def cover(task):
    print("Start cover")
    time.sleep(5)
    current = 0
    task.plotter.send_pos(pts[current][0], pts[current][1])
    print('Next point ' + str(pts[current]))
    while task._running:
        if task.plotter.has_reached_pos():
            current += 1
            if current > 4:
                break
            print('Next point ' + str(pts[current]))
            task.plotter.send_pos(pts[current][0], pts[current][1])

    # send stop
    task.plotter.send_xy(0, 0)
    print("Stopped cover")

def back_forth(task):
    print("Start back and forth")
    time.sleep(5)
    x = LIMIT_MIN_X
    y = LIMIT_MIN_Y
    up = False
    task.plotter.send_pos(x, y)
    while task._running:
        if task.plotter.has_reached_pos():
            if up:
                y += 20.0
                if y > LIMIT_MAX_Y:
                    break
            else:
                if x == LIMIT_MIN_X:
                    x = LIMIT_MAX_X
                else:
                    x = LIMIT_MIN_X

            task.plotter.send_pos(x, y)
            up = not up

    # send stop
    task.plotter.send_xy(0, 0)
    print("Stopped back and forth")