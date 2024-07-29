from kivy.app import App
from kivy.uix.label import Label
from jnius import autoclass, PythonJavaClass, java_method
import os

# Set up the Java classes needed for observing SMS
Context = autoclass('android.content.Context')
ContentResolver = autoclass('android.content.ContentResolver')
Uri = autoclass('android.net.Uri')
Cursor = autoclass('android.database.Cursor')
Looper = autoclass('android.os.Looper')
Handler = autoclass('android.os.Handler')
ContentObserver = autoclass('android.database.ContentObserver')
Intent = autoclass('android.content.Intent')
MediaPlayer = autoclass('android.media.MediaPlayer')
RingtoneManager = autoclass('android.media.RingtoneManager')
AudioManager = autoclass('android.media.AudioManager')

# Define the SMS observer class
class SmsObserver(PythonJavaClass):
    __javainterfaces__ = ['android/database/ContentObserver']

    def __init__(self, handler):
        super(SmsObserver, self).__init__(handler)

    @java_method('()V')
    def onChange(self, selfChange):
        self.on_sms_received()

    def on_sms_received(self):
        context = App.get_running_app().context
        content_resolver = context.getContentResolver()
        uri = Uri.parse("content://sms/inbox")
        cursor = content_resolver.query(uri, None, None, None, "_id DESC")

        if cursor.moveToFirst():
            body = cursor.getString(cursor.getColumnIndex("body"))
            if "YOUR_KEYWORD" in body:
                self.play_sound()

    def play_sound(self):
        context = App.get_running_app().context
        audio_manager = context.getSystemService(Context.AUDIO_SERVICE)
        max_volume = audio_manager.getStreamMaxVolume(AudioManager.STREAM_ALARM)
        audio_manager.setStreamVolume(AudioManager.STREAM_ALARM, max_volume, 0)

        media_player = MediaPlayer()
        media_player.setDataSource(context, RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM))
        media_player.setAudioStreamType(AudioManager.STREAM_ALARM)
        media_player.prepare()
        media_player.start()

class SMSApp(App):
    def build(self):
        self.context = Context.getApplicationContext()
        handler = Handler(Looper.getMainLooper())
        observer = SmsObserver(handler)
        uri = Uri.parse("content://sms")
        self.context.getContentResolver().registerContentObserver(uri, True, observer)
        return Label(text="SMS Observer Running")

if __name__ == '__main__':
    SMSApp().run()
