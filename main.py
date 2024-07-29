from kivy.app import App
from kivy.uix.label import Label
from jnius import autoclass, cast

class MainApp(App):
    def build(self):
        self.start_service()
        return Label(text="SMS Observer Running")

    def start_service(self):
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        service = autoclass('org.kivy.android.PythonService')

        mActivity = PythonActivity.mActivity
        context = cast('android.content.Context', mActivity.getApplicationContext())

        serviceIntent = Intent(context, service)
        mActivity.startService(serviceIntent)

if __name__ == '__main__':
    MainApp().run()
