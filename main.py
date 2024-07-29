from kivy.app import App
from kivy.uix.label import Label
from jnius import autoclass

class MainApp(App):
    def build(self):
        self.start_service()
        return Label(text="SMS Observer Running")

    def start_service(self):
        service = autoclass('org.kivy.android.PythonService')
        mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
        argument = ''
        service.start(mActivity, argument)

if __name__ == '__main__':
    MainApp().run()
