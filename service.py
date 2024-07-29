from kivy.app import App
from jnius import autoclass, PythonJavaClass, java_method
from android.runnable import run_on_ui_thread
import os

# Set up the Java classes needed for observing SMS
PythonService = autoclass('org.kivy.android.PythonService')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Context = autoclass('android.content.Context')
Uri = autoclass('android.net.Uri')
Cursor = autoclass('android.database.Cursor')
Looper = autoclass('android.os.Looper')
Handler = autoclass('android.os.Handler')
ContentObserver = autoclass('android.database.ContentObserver')
MediaPlayer = autoclass('android.media.MediaPlayer')
RingtoneManager = autoclass('android.media.RingtoneManager')
AudioManager = autoclass('android.media.AudioManager')

class SmsObserver(PythonJavaClass):
    __javainterfaces__ = ['android/database/ContentObserver']

    def __init__(self, handler):
        super(SmsObserver, self).__init__(handler)

    @java_method('()V')
    def onChange(self, selfChange):
        self.on_sms_received()

    def on_sms_received(self):
        context = PythonService.mService.getApplicationContext()
        content_resolver = context.getContentResolver()
        uri = Uri.parse("content://sms/inbox")
        cursor = content_resolver.query(uri, None, None, None, "_id DESC")

        if cursor.moveToFirst():
            body = cursor.getString(cursor.getColumnIndex("body"))
            if "YOUR_KEYWORD" in body:
                self.play_sound()

    def play_sound(self):
        context = PythonService.mService.getApplicationContext()
        audio_manager = context.getSystemService(Context.AUDIO_SERVICE)
        max_volume = audio_manager.getStreamMaxVolume(AudioManager.STREAM_ALARM)
        audio_manager.setStreamVolume(AudioManager.STREAM_ALARM, max_volume, 0)

        media_player = MediaPlayer()
        media_player.setDataSource(context, RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM))
        media_player.setAudioStreamType(AudioManager.STREAM_ALARM)
        media_player.prepare()
        media_player.start()

class SMSService(PythonService):
    def onCreate(self):
        super(SMSService, self).onCreate()
        handler = Handler(Looper.getMainLooper())
        observer = SmsObserver(handler)
        uri = Uri.parse("content://sms")
        self.getContentResolver().registerContentObserver(uri, True, observer)

    def onStartCommand(self, intent, flags, startId):
        return super(SMSService, self).onStartCommand(intent, flags, startId)

if __name__ == '__main__':
    from kivy.utils import platform
    if platform == 'android':
        from android import AndroidService
        service = AndroidService('SMS Observer', 'running')
        service.start('service started')
    else:
        from kivy.app import App
        from kivy.uix.label import Label
        class TestApp(App):
            def build(self):
                return Label(text='SMS Observer Running')
        TestApp().run()
