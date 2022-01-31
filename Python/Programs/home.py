def home(task):
    print("Start homing")

    task.plotter.send_pos(0, 0)

    while task._running:
        if task.plotter.has_reached_pos():
            print ("Home reached")

    # send stop
    task.plotter.send_xy(0, 0)
    print("Stopped homing")