import time
import cv2
from Programs.camera_feed import create_capture, process_frame, sigmoid_01, map_brightness

print("Starting camera feed")

capture = create_capture()
time.sleep(1)

last_start = time.time()

while True:
    ret, frame = capture.read()
    processed, frame, val = process_frame(frame)
    processed =  cv2.resize(processed, (256, 256))

    delay = map_brightness(0.06, 6.0, val)

    curr_interval = (time.time() - last_start)
    if curr_interval > delay:
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

    cv2.imshow('processed', processed)
    cv2.imshow('frame', frame)

    #exit if ESC is pressed
    c = cv2.waitKey(1)
    if c == 27:
        break        

capture.release()
cv2.destroyAllWindows()

print("Stopped camera feed")