import sys
sys.path.append('snowboy/')
import snowboydecoder
import signal
from aiy.audio import play_wave
import os
import nabaztagActions
from wit import Wit

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
if len(sys.argv) != 3:
    print('usage: python ' + sys.argv[0] + ' <wit-token>')
    exit(1)


def wit_speech_to_text():
    access_token = sys.argv[2]
    nabaztagActions.earsPayAttention()
    print('Listening command...')
    listening = True
    client = Wit(access_token=access_token)
    client.interactive(handle_message=handle_message)

def action_echo(textToSay):
    nabaztagActions.sayMan(textToSay)


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
    detector.start(detected_callback=wit_speech_to_text,
                interrupt_check=interrupt_callback,
                sleep_time=0.03)
    detector.terminate()

def handle_message(response):
    print(response['entities'])
    print(response)



