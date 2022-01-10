# Sends xy command to arduino
def send_xy(arduino, x , y):
    sendStr = "{0} {1}\n".format(x, y)
    arduino.write(bytes(sendStr, 'utf-8'))
    print("[SEND] " + sendStr, end= '')
    res = arduino.readline().decode("utf-8").replace('\n', '')
    if(len(res) > 0):
        print("[ARDUINO] " + res)