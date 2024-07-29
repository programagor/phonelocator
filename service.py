# service.py
from jnius import autoclass, PythonJavaClass, java_method
import time

PythonService = autoclass('org.kivy.android.PythonService')
ContentResolver = autoclass('android.content.ContentResolver')
Uri = autoclass('android.net.Uri')
Looper = autoclass('android.os.Looper')

class SMSObserver(PythonJavaClass):
    __javainterfaces__ = ['android/database/ContentObserver']
    
    def __init__(self):
        super().__init__(self, None)
        self.context = PythonService.mService.getApplicationContext()
        self.content_resolver = self.context.getContentResolver()
    
    @java_method('()V')
    def startObserving(self):
        uri = Uri.parse("content://sms")
        self.content_resolver.registerContentObserver(uri, True, self)
    
    @java_method('(Z)V')
    def onChange(self, selfChange):
        self.readSMS()
    
    def readSMS(self):
        cursor = self.content_resolver.query(Uri.parse("content://sms/inbox"), None, None, None, None)
        if cursor and cursor.moveToFirst():
            body = cursor.getString(cursor.getColumnIndex("body"))
            if "ALERT" in body:
                self.trigger_beep()
        if cursor:
            cursor.close()

    def trigger_beep(self):
        RingtoneManager = autoclass('android.media.RingtoneManager')
        AudioManager = autoclass('android.media.AudioManager')
        Context = autoclass('android.content.Context')
        
        audio_manager = self.context.getSystemService(Context.AUDIO_SERVICE)
        audio_manager.setStreamVolume(AudioManager.STREAM_MUSIC, audio_manager.getStreamMaxVolume(AudioManager.STREAM_MUSIC), 0)
        ringtone = RingtoneManager.getRingtone(self.context, RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM))
        ringtone.play()

def start():
    observer = SMSObserver()
    observer.startObserving()
    while True:
        time.sleep(1)

start()
