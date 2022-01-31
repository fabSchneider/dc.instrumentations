import time
import math
import random

def random_walk(task):
    print("Starting random walk")
    dir = random.uniform(-math.pi, math.pi)
    while task._running:
        dir += random.uniform(-math.pi * 0.5, math.pi * 0.5)
        x = math.cos(dir)
        y = math.sin(dir)
        task.plotter.send_xy(x, y)
        time.sleep(0.5)

    # send stop
    task.plotter.send_xy(0, 0)
    print("Stopped random walks")

def random_walk_sequence(task):
    print("Starting random walk")
    # dir = random.uniform(-math.pi, math.pi)
    dir = random.randint(0, 3) * math.pi * 0.5

    sequence = [0.1, 0.3, 0.6, 1, 3, 6]

    start_time = time.time()
    seq_id = 0
    seq_dir = 1
    interval_len = 13.0
    while task._running:
        # dir += random.uniform(-math.pi * 1.0, math.pi * 1.0)
        dir += random.randint(0, 3) * math.pi * 0.5
        x = math.cos(dir)
        y = math.sin(dir)
        task.plotter.send_xy(x, y)
        time.sleep(sequence[seq_id])
        curr_interval = time.time() - start_time
        if(curr_interval > interval_len):
            start_time = time.time()
            if(seq_id == len(sequence) - 1):
                seq_dir = -1
            elif(seq_id == 0):
                seq_dir = 1      
            seq_id = seq_id + seq_dir
            print("Starting Generation " + str(seq_id))

    # send stop
    task.plotter.send_xy(0, 0)
    print("Stopped random walk sequence")