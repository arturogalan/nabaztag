import sys
sys.path.append('snowboy/')
import snowboydecoder
import signal
from aiy.audio import play_wave
import aiy.cloudspeech
import os
import aiy.assistant.auth_helpers
from aiy.assistant.library import Assistant
import nabaztagActions

recognizer = aiy.cloudspeech.get_recognizer()
interrupted = False
TOP_DIR = os.path.dirname(os.path.abspath(__file__))
DETECT_DING = os.path.join(TOP_DIR, "resources/ding.wav")


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)



def gcloud_speech_to_text():
    nabaztagActions.earsPayAttention()
    global recognizer
    print('Listening command...')
    listening = True
    while listening:
        text = recognizer.recognize()
        nabaztagActions.earsActionDone()
        if not text:
            print('Sorry, I did not hear you.')
        else:
            print('You said "', text, '"')
            action_echo(text)
            listening = False

def action_echo(textToSay):
    nabaztagActions.sayWoman(textToSay)


def test():
    print('test')
# main loop
# credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
# with Assistant(credentials) as assistant:
def startRecognizer():
    model = sys.argv[1]
    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.55, audio_gain=1)
    print('Nabaztag listening... Press Ctrl+C to exit')
    # recognizer = aiy.cloudspeech.get_recognizer()
    aiy.audio.get_recorder().start()
    detector.start(detected_callback=gcloud_speech_to_text,
                interrupt_check=interrupt_callback,
                sleep_time=0.03)
    detector.terminate()
