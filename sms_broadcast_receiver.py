from jnius import autoclass, PythonJavaClass, java_method
from plyer import notification

Intent = autoclass('android.content.Intent')
BroadcastReceiver = autoclass('android.content.BroadcastReceiver')
SMS_RECEIVED = autoclass('android.provider.Telephony$Sms.Intents').SMS_RECEIVED
AudioManager = autoclass('android.media.AudioManager')
Context = autoclass('android.content.Context')
RingtoneManager = autoclass('android.media.RingtoneManager')

class SMSReceiver(PythonJavaClass):
    __javainterfaces__ = ['android/content/BroadcastReceiver']

    @java_method('(Landroid/content/Context;Landroid/content/Intent;)V')
    def onReceive(self, context, intent):
        if intent.getAction() == SMS_RECEIVED:
            pdus = intent.getExtras().get('pdus')
            messages = []
            for pdu in pdus:
                message = autoclass('android.telephony.SmsMessage').createFromPdu(pdu)
                messages.append(message.getMessageBody())
            sms_content = ''.join(messages)
            keyword = "ALERT"  # Your specific keyword
            if keyword in sms_content:
                self.trigger_beep(context)

    def trigger_beep(self, context):
        audio_manager = context.getSystemService(Context.AUDIO_SERVICE)
        audio_manager.setStreamVolume(AudioManager.STREAM_MUSIC, audio_manager.getStreamMaxVolume(AudioManager.STREAM_MUSIC), 0)
        ringtone = RingtoneManager.getRingtone(context, RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM))
        ringtone.play()

# Register the receiver
receiver = SMSReceiver()
context = PythonService.mService.getApplicationContext()
intent_filter = autoclass('android.content.IntentFilter')(SMS_RECEIVED)
context.registerReceiver(receiver, intent_filter)
