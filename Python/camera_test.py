import time
import cv2

def process_frame(frame):

    crop = 16
    frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    frame_bw = cv2.GaussianBlur(frame_bw,(21,21),0)

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


print("Starting camera feed")

capture = cv2.VideoCapture(-1)
time.sleep(1)

capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
capture.set(cv2.CAP_PROP_EXPOSURE, 105)

last_start = time.time()

while True:
    ret, frame = capture.read()
    processed, frame, val = process_frame(frame)
    processed =  cv2.resize(processed, (256, 256))

    delay = (1.0 - val) * 5.0 + 0.03

    curr_interval = (time.time() - last_start)
    if curr_interval > delay:
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

    cv2.imshow('processed', processed)
    cv2.imshow('frame', frame)

    #exit if ESC is pressed
    c = cv2.waitKey(1)
    if c == 27:
        break        

capture.release()
cv2.destroyAllWindows()

print("Stopped camera feed")