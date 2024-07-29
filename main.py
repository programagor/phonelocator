# main.py
from kivy.app import App
from kivy.uix.label import Label
from jnius import autoclass
from android import mActivity

class SMSListenerApp(App):
    def build(self):
        self.start_service('Smslistener')
        return Label(text="SMS Listener App Running")

    def start_service(self, name):
        context = mActivity.getApplicationContext()
        service_name = str(context.getPackageName()) + '.Service' + name
        service = autoclass(service_name)
        service.start(mActivity, '')   # starts or re-initializes a service

if __name__ == '__main__':
    SMSListenerApp().run()
