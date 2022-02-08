import time
import math
import cv2
import random

def camera_feed(task):
    print("Starting camera feed")

    capture = cv2.VideoCapture(0)
    time.sleep(1)

    capture.set(cv2.CAP_PROP_SETTINGS, 0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    capture.set(cv2.CAP_PROP_EXPOSURE, 30)

    dir = random.uniform(-math.pi, math.pi)

    last_start = time.time()

    try:
        while task._running:
            ret, frame = capture.read()
            processed, val = process_frame(frame)
            processed =  cv2.resize(processed, (256, 256))

            delay = (1.0 - min(val * 1.5, 1)) * 5.0 + 0.03

            curr_interval = (time.time() - last_start)
            if curr_interval > delay:
                dir += random.uniform(-math.pi * 0.5, math.pi * 0.5)
                x = math.cos(dir)
                y = math.sin(dir)
                task.plotter.send_xy(x, y)
                last_start = time.time()

            cv2.putText(
                processed, str(val), (8, 16), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 1)
            cv2.putText(
                processed, str(delay), (8, 32), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 1)
            cv2.putText(
                processed, str(curr_interval), (8, 48), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 1)
            cv2.imshow('video', processed)
            cv2.waitKey(1)          
    except Exception as ex:
        print(ex)

    capture.release()
    cv2.destroyAllWindows()

    # send stop
    task.plotter.send_xy(0, 0)
    print("Stopped camera feed")

def process_frame(frame):
    processed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    size = 8
    processed = cv2.resize(processed, (size, size))
    sum = 0.0
    for x in range(0, size):
        for y in range(0, size):
            sum += processed[x, y]

    val = (sum / (size * size)) / 255
    return processed, val