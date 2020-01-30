import sys
sys.path.append('snowboy/')
import snowboydecoder
import signal
import os
import nabaztagActions
from wit import Wit

import argparse
import time
import threading

from aiy.board import Board
from aiy.voice.audio import AudioFormat, play_wav, record_file, Recorder
import requests
import json

API_ENDPOINT = 'https://api.wit.ai/speech'
ACCESS_TOKEN = ''

# python3 nabaztag.py Alice.pmdl 

interrupted = False
TOP_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_WAV_FILE = "recording.wav"
done = threading.Event()

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

def wait():
    start = time.monotonic()
    duration = time.monotonic() - start
    
    while duration < 4:
        duration = time.monotonic() - start
        print('Recording: %.02f seconds [Press button to stop]' % duration)
        time.sleep(0.5)
def wit_speech_to_text():
    global done
    with Board() as board:
        access_token = sys.argv[2]
        nabaztagActions.earsPayAttention()
        print('Listening command...with token', access_token)
        listening = True
        board.button.when_pressed = done.set
        record_file(AudioFormat.CD, filename=TEMP_WAV_FILE, wait=wait, filetype='wav')
        board.button.wait_for_press(timeout=4)
        print('4 seconds...playing: ', TEMP_WAV_FILE)
        # play_wav(TEMP_WAV_FILE)
        audio = read_audio(TEMP_WAV_FILE)
        # defining headers for HTTP request
        headers = {'authorization': 'Bearer ' + ACCESS_TOKEN,
                'Content-Type': 'audio/wav'}

        #Send the request as post request and the audio as data
        resp = requests.post(API_ENDPOINT, headers = headers,
                                data = audio)

        #Get the text
        data = json.loads(resp.content)
        print(data)
        action_echo(data['_text'])
        interrupted = true
    # client = Wit(access_token=access_token)
    # client.interactive(handle_message=handle_message)

def read_audio(WAVE_FILENAME):
    # function to read audio(wav) file
    with open(WAVE_FILENAME, 'rb') as f:
        audio = f.read()
    return audio

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
    detector.start(detected_callback=wit_speech_to_text,
                interrupt_check=interrupt_callback,
                sleep_time=0.03)
    detector.terminate()

def handle_message(response):
    print(response['entities'])
    print(response)



