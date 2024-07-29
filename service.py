# service.py
from jnius import autoclass, PythonJavaClass, java_method
import time

PythonService = autoclass('org.kivy.android.PythonService')
Context = autoclass('android.content.Context')
Intent = autoclass('android.content.Intent')
BroadcastReceiver = autoclass('android.content.BroadcastReceiver')
SmsMessage = autoclass('android.telephony.SmsMessage')
RingtoneManager = autoclass('android.media.RingtoneManager')
AudioManager = autoclass('android.media.AudioManager')
IntentFilter = autoclass('android.content.IntentFilter')

class SMSReceiver(PythonJavaClass):
    __javainterfaces__ = ['android/content/BroadcastReceiver']

    @java_method('(Landroid/content/Context;Landroid/content/Intent;)V')
    def onReceive(self, context, intent):
        if intent.getAction() == 'android.provider.Telephony.SMS_RECEIVED':
            pdus = intent.getExtras().get('pdus')
            messages = []
            for pdu in pdus:
                message = SmsMessage.createFromPdu(pdu)
                messages.append(message.getMessageBody())
            sms_content = ''.join(messages)
            keyword = "ALERT"
            if keyword in sms_content:
                self.trigger_beep(context)

    def trigger_beep(self, context):
        audio_manager = context.getSystemService(Context.AUDIO_SERVICE)
        audio_manager.setStreamVolume(AudioManager.STREAM_MUSIC, audio_manager.getStreamMaxVolume(AudioManager.STREAM_MUSIC), 0)
        ringtone = RingtoneManager.getRingtone(context, RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM))
        ringtone.play()

def start_service():
    context = PythonService.mService.getApplicationContext()
    receiver = SMSReceiver()
    intent_filter = IntentFilter('android.provider.Telephony.SMS_RECEIVED')
    context.registerReceiver(receiver, intent_filter)
    while True:
        time.sleep(1)

start_service()
