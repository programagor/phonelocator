# service.py
from jnius import autoclass
import time

PythonService = autoclass('org.kivy.android.PythonService')

def start():
    PythonService.mService.setAutoForeground()
    while True:
        time.sleep(1)

start()
