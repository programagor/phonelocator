from jnius import autoclass
import time

Intent = autoclass('android.content.Intent')
BroadcastReceiver = autoclass('android.content.BroadcastReceiver')
Service = autoclass('org.kivy.android.PythonService')
PythonService = autoclass('org.kivy.android.PythonService')

def start():
    PythonService.mService.setAutoForeground()
    context = PythonService.mService.getApplicationContext()
    intent = Intent(context, autoclass('org.kivy.android.PythonService'))
    context.startService(intent)

start()
while True:
    time.sleep(1)
