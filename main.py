from kivy.app import App
from kivy.uix.label import Label
from jnius import autoclass, cast

PythonService = autoclass('org.kivy.android.PythonService')
Context = autoclass('android.content.Context')
Intent = autoclass('android.content.Intent')
PendingIntent = autoclass('android.app.PendingIntent')
AlarmManager = autoclass('android.app.AlarmManager')

class SMSListenerApp(App):
    def build(self):
        # Start the background service
        if not PythonService.mService:
            self.start_service()
        return Label(text="SMS Listener App Running")

    def start_service(self):
        service_intent = Intent(self.get_service_context(), self.get_service_class())
        PendingIntent.getService(self.get_service_context(), 0, service_intent, PendingIntent.FLAG_UPDATE_CURRENT)
        context = self.get_service_context()
        context.startService(service_intent)

    def get_service_context(self):
        return cast('android.content.Context', PythonService.mService.getApplicationContext())

    def get_service_class(self):
        return cast('java.lang.Class', autoclass('org.kivy.android.PythonService'))

if __name__ == '__main__':
    SMSListenerApp().run()
