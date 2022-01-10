from serial.serialutil import SerialException
import gamepad
import math
import time
import serial

# arduino serial settings
port = 'COM5'
baudrate = 115200

# the frequency at which the gamepad is polled for input (in seconds)
gamepad_polling_freq = 0.03

# Sends xy command to arduino
def send_xy(arduino, x , y):
    sendStr = "{0} {1}\n".format(x, y)
    arduino.write(bytes(sendStr, 'utf-8'))
    print("[SEND] " + sendStr, end= '')
    print("[ARDUINO] " + arduino.readline().decode("utf-8").replace('\n', ''))

# clamps a vector to be within the unit circle
def clamp_to_unit(x, y):
    mag = math.sqrt(pow(x, 2) + pow(y, 2))

    if (mag > 0) :
        x = x / mag * min(mag, 1)
        y = y / mag * min(mag, 1)
    
    return x, y

# starts sending data to arduino
def run_send(gamepad, arduino):
    print("Starting to send data from the gamepad to arduino on port {0} (baudrate: {1})".format(port, baudrate))
    last_x = math.nan
    last_y = math.nan
    # start the send loop
    while True:
        if(not gamepad.is_running()):
            send_xy(arduino, 0, 0)
            return "disconnect"
        if gamepad.X == 1:
            send_xy(arduino, 0, 0)
            return "stopped"

        x = gamepad.RightJoystickX
        # invert y to match direction the pen is moving more closely
        y = gamepad.RightJoystickY
        
        x, y = clamp_to_unit(x, y)
        
        if x != last_x or y != last_y :
            last_x = x
            last_y = y
            send_xy(arduino, x, y)

        time.sleep(gamepad_polling_freq)

if __name__ == '__main__':

    # create the gamepad listener
    gpad = gamepad.Gamepad()

    try:
        arduino = serial.Serial(port, baudrate, timeout = 0.003)
        res = run_send(gpad, arduino)   

        if res == "disconnected":
            print("gamepad disconnected")
        if res == "stopped":
            print("sending stopped")

        arduino.close()    
    except SerialException as e:
        print (e)       
   


