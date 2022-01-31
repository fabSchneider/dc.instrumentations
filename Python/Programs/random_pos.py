import random
import time

def random_star(task):
    print("Start random pos")

    range = 200

    x = random.uniform(-range, range)
    y = random.uniform(-range, range)
    task.plotter.send_pos(x, y)

    homing = False

    while task._running:
        if task.plotter.has_reached_pos(): 
            if homing:
                print ("Reached home")        
                x = random.uniform(-range, range)
                y = random.uniform(-range, range)
                task.plotter.send_pos(x, y)
                homing = False
            else:
                print ("Reached target")
                task.plotter.send_pos(0, 0)
                homing = True

    # send stop
    task.plotter.send_xy(0, 0)
    print("Stopped ranomd pos")

def random_brush(task):
    print("Start random brush")

    pickup_x = 0
    pickup_Y = -520

    range = 400


    task.plotter.send_pos(pickup_x, pickup_x)

    homing = True

    while task._running:
        if task.plotter.has_reached_pos(): 
            if homing:
                print ("Reached pickup")   
                time.sleep(1.0) 
                x = random.uniform(0, range)
                y = random.uniform(0, range)
                task.plotter.send_pos(x, y)
                homing = False
            else:
                print ("Reached target")
                task.plotter.send_pos(pickup_x, pickup_Y)
                homing = True

    # send stop
    task.plotter.send_xy(0, 0)
    print("Stopped ranomd brush")
    