from ctypes import windll, Structure, c_uint, sizeof, byref

class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]

class InputMonitor:

    def __init__(self):
    	self.last_tick_count = windll.kernel32.GetTickCount()

    def active(self):
    	last_input_info = LASTINPUTINFO()
        last_input_info.cbSize = sizeof(last_input_info)
        windll.user32.GetLastInputInfo(byref(last_input_info))
    	activenow = last_input_info.dwTime > self.last_tick_count
        self.last_tick_count = windll.kernel32.GetTickCount()
        return activenow