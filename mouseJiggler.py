import pyautogui
import random
import time
import threading
import ctypes

class MouseJiggler:
    def __init__(self):
        self.running = False
        self.stop_event = threading.Event()
        self.thread = None
        # New attribute to enable auto inactivity detection.
        self.auto_detection = False

    def get_idle_duration(self):
        # Returns idle time in seconds.
        class LASTINPUTINFO(ctypes.Structure):
            _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]
        lastInputInfo = LASTINPUTINFO()
        lastInputInfo.cbSize = ctypes.sizeof(lastInputInfo)
        ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lastInputInfo))
        millis = ctypes.windll.kernel32.GetTickCount() - lastInputInfo.dwTime
        return millis / 1000.0

    def jiggle(self):
        while not self.stop_event.is_set():
            if self.auto_detection:
                idle = self.get_idle_duration()
                # Only jiggle if user idle for 60+ seconds.
                if idle < 60:
                    time.sleep(1)
                    continue
            # Get current mouse position.
            current_x, current_y = pyautogui.position()
            # Generate random offsets.
            offset_x = random.choice([-1, 1]) * random.randint(60, 100)
            offset_y = random.choice([-1, 1]) * random.randint(60, 100)
            pyautogui.moveRel(offset_x, offset_y, duration=0.3)
            pyautogui.moveTo(current_x, current_y, duration=0.3)
            pyautogui.keyDown('shift')
            time.sleep(0.1)
            pyautogui.keyUp('shift')
            if self.auto_detection:
                # Check more frequently when in auto mode.
                time.sleep(1)
            else:
                time.sleep(5)

    def start(self):
        if not self.running:
            self.stop_event.clear()
            self.thread = threading.Thread(target=self.jiggle, daemon=True)
            self.thread.start()
            self.running = True

    def stop(self):
        if self.running:
            self.stop_event.set()
            self.thread.join()
            self.running = False
