from inputs import UnpluggedError, get_gamepad
import math
import threading

class Gamepad(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    JOY_DEADZONE = 0.3
    TRIG_DEADZONE = 0.3

    def __init__(self):
        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def is_running(self):
        return self._monitor_thread.is_alive()

    def _monitor_controller(self):
        while True:
            try:
                events = get_gamepad()
            except UnpluggedError as e:
                print(e)
                return

            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = self._process_deadzone(event.state / Gamepad.MAX_JOY_VAL, Gamepad.JOY_DEADZONE) # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = self._process_deadzone(event.state / Gamepad.MAX_JOY_VAL, Gamepad.JOY_DEADZONE) # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = self._process_deadzone(event.state / Gamepad.MAX_JOY_VAL, Gamepad.JOY_DEADZONE) # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = self._process_deadzone(event.state / Gamepad.MAX_JOY_VAL, Gamepad.JOY_DEADZONE) # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger =  self._process_deadzone(event.state / Gamepad.MAX_JOY_VAL, Gamepad.TRIG_DEADZONE) # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = self._process_deadzone(event.state / Gamepad.MAX_JOY_VAL, Gamepad.TRIG_DEADZONE) # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state
                elif event.code == 'BTN_WEST':
                    self.X = event.state
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state

    def _map_range(self, value, inMin, inMax, outMin, outMax):
        return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))

    def _process_deadzone(self, val, deadzone):
        if(val > deadzone):
            return self._map_range(val, deadzone, 1, 0, 1)
        elif (val < -deadzone):
            return self._map_range(val, -1, -deadzone, -1, 0)
        else:
            return 0
