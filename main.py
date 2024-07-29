# main.py
from kivy.app import App
from kivy.uix.label import Label
from jnius import autoclass, cast

PythonService = autoclass('org.kivy.android.PythonService')
Context = autoclass('android.content.Context')
Intent = autoclass('android.content.Intent')
PythonActivity = autoclass('org.kivy.android.PythonActivity')

class SMSListenerApp(App):
    def build(self):
        self.start_service()
        return Label(text="SMS Listener App Running")

    def start_service(self):
        # Start the background service if it's not already running
        service_class = autoclass('org.kivy.android.PythonService')
        service_intent = Intent(PythonActivity.mActivity, service_class)
        PythonActivity.mActivity.startService(service_intent)

if __name__ == '__main__':
    SMSListenerApp().run()
