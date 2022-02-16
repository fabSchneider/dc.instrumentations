import time
import math
import cv2
import random
import numpy as np

video_id = -1
cap_width = 320
cap_height = 240
cap_exposure = 115

def process_frame(frame):

    crop = 8
    frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    frame_bw = cv2.GaussianBlur(frame_bw,(11,11),0)

    frame_y = int(frame_bw.shape[0] * 0.8 - (crop / 2))
    frame_x = int(frame_bw.shape[1] / 2 - (crop / 2)) + 8

    processed = frame_bw[frame_y:frame_y+crop, frame_x:frame_x+crop]
    size = crop
    processed = cv2.resize(processed, (size, size))
    sum = 0.0
    for x in range(0, size):
        for y in range(0, size):
            sum += processed[x, y]

    val = (sum / (size * size)) / 255
    cv2.rectangle(frame_bw, (frame_x, frame_y), (frame_x + crop, frame_y + crop), color = 20, thickness=1)
    return processed, frame_bw, val

def sigmoid_01(x, s):
    return 1.0 / (1.0 + math.e**(-x*s + s/2))

def map_brightness(_min, _max, b):
    b = sigmoid_01(b, 10)
    return (1.0 - b) * _max + _min

def create_capture():
    capture = cv2.VideoCapture(video_id)
    time.sleep(1)

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)
    if(cap_exposure == -1):
        capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
    else:
        capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        capture.set(cv2.CAP_PROP_EXPOSURE, cap_exposure)

    return capture

def camera_feed(task):
    print("Starting camera feed")
    random.seed(999)
    capture = create_capture()

    # dir = random.uniform(-math.pi, math.pi)
    dir = random.randint(0, 3) * math.pi * 0.5

    last_start = time.time()

    try:
        while task._running:
            ret, frame = capture.read()
            processed, frame, val = process_frame(frame)
            processed =  cv2.resize(processed, (256, 256))

            delay = map_brightness(0.06, 6.0, val)

            curr_interval = (time.time() - last_start)
            if curr_interval > delay:
                dir += random.randint(0, 3) * math.pi * 0.5
                # dir += random.uniform(-math.pi * 0.5, math.pi * 0.5)
                x = math.cos(dir)
                y = math.sin(dir)
                task.plotter.send_xy(x, y)
                last_start = time.time()

            ui_color = 255
            if val > 0.7:
                ui_color = 0

            cv2.putText(
                processed, str(val), (8, 16), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, ui_color, 1)
            cv2.putText(
                processed, str(delay), (8, 32), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, ui_color, 1)
            cv2.putText(
                processed, str(curr_interval), (8, 48), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, ui_color, 1)
            cv2.line(processed, (0,245), (int(255 * (delay/6.0)), 245), ui_color, 5)
            cv2.imshow('frame', frame)
            cv2.imshow('processed', processed)
            cv2.waitKey(1)          
    except Exception as ex:
        print(ex)

    capture.release()
    cv2.destroyAllWindows()

    # send stop
    task.plotter.send_xy(0, 0)
    print("Stopped camera feed")

def camera_feed_circles(task):
    print("Starting camera feed circles")

    capture = create_capture()

    dir = random.uniform(-math.pi, math.pi)

    cc = True
    last_start = time.time()
    delay = 0
    val = 0
    processed = np.zeros((256, 256, 1))
    try:
        while task._running:
            curr_interval = (time.time() - last_start)
            ret, frame = capture.read()

            if curr_interval > delay:
                processed, frame, val = process_frame(frame)

                delay = map_brightness(0.1, 5, val)
                last_start = time.time()
                cc = random.choice([True, False])
                dir = -dir
            if(cc):
                dir += sigmoid_01(val, 5) * 0.06
            else:
                dir -= sigmoid_01(val, 5) * 0.06


            processed_show =  cv2.resize(processed, (256, 256))
            cv2.putText(
                processed_show, str(val), (8, 16), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 1)
            cv2.putText(
                processed_show, str(delay), (8, 32), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 1)
            cv2.putText(
                processed_show, str(curr_interval), (8, 48), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 1)

            cv2.imshow('processed', processed_show)

            x = math.cos(dir)
            y = math.sin(dir)
            task.plotter.send_xy(x, y)
            cv2.imshow('frame', frame)

            cv2.waitKey(3)          
    except Exception as ex:
        print(ex)

    capture.release()
    cv2.destroyAllWindows()

    # send stop
    task.plotter.send_xy(0, 0)
    print("Stopped camera feed circles")