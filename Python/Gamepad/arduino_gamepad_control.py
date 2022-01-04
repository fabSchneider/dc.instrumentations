import gamepad
import math
import time
import serial

# arduino serial settings
port = 'COM5'
baudrate = 115200

# the frequency at which the gamepad is polled for input (in seconds)
gamepad_polling_freq = 0.03

# Send command to arduino
def send(arduino, x , y):
    sendStr = "{0} {1}\n".format(x, y)
    arduino.write(bytes(sendStr, 'utf-8'))
    print("[SEND] " + sendStr, end= '')
    print("[ARDUINO] " + arduino.readline().decode("utf-8"))

# sends a stop command to the arduino
def stop(arduino):
    arduino.write(bytes("0 0", 'utf-8'))

# clamps a vector to be within the unit circle
def clamp_to_unit(x, y):
    mag = math.sqrt(pow(x, 2) + pow(y, 2))

    if (mag > 0) :
        x = x / mag * min(mag, 1)
        y = y / mag * min(mag, 1)
    
    return x, y

def send_loop(gamepad, arduino):

    last_x = math.nan
    last_y = math.nan

    while gamepad.is_running():
                        
        if(gamepad.X == 1):
            # send stop data to arduino before stopping
            stop(arduino)
            return
        
        x = gamepad.RightJoystickX
        # invert y to match direction the pen is moving more closely
        y = gamepad.RightJoystickY
        
        x, y = clamp_to_unit(x, y)
        
        if x != last_x or y != last_y :
            last_x = x
            last_y = y
            send(arduino, x, y)

        time.sleep(gamepad_polling_freq)

if __name__ == '__main__':

    # create the gamepad listener
    gpad = gamepad.Gamepad()
    with serial.Serial(port, baudrate) as arduino :
        # wait for first response from arduino
        arduino.readline()
        if gpad.is_running():
            print("Starting to send data from the gamepad to arduino on port {0} (baudrate: {1})".format(port, baudrate))
            # start the send loop
            send_loop(gpad, arduino)         
            print("Sending stopped")
        print("Quitting...")  


   


