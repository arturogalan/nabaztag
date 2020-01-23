#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run a recognizer using the Google Assistant Library.

The Google Assistant Library has direct access to the audio API, so this Python
code doesn't need to record audio. Hot word detection "OK, Google" is supported.

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""

import logging
import platform
import subprocess
import sys

import aiy.assistant.auth_helpers
from aiy.assistant.library import Assistant
import aiy.audio
import aiy.voicehat
from google.assistant.library.event import EventType

import vlc
global vlc_volume
vlc_volume = 100

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)


def power_off_pi():
    aiy.audio.say('Good bye!')
    subprocess.call('sudo shutdown now', shell=True)


def reboot_pi():
    aiy.audio.say('See you in a bit!')
    subprocess.call('sudo reboot', shell=True)


def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    aiy.audio.say('Mi dirección IP es %s' % ip_address.decode('utf-8'))

def radiostop():
    try:
        player.stop()
    except NameError as e:
        print("Error la radio no se ha encendido!")

def radiovoldown():
    try:
        global vlc_volume
        vlc_volume = vlc_volume-10
        print("Radio Volume: %s ", vlc_volume)
        player.audio_set_volume(vlc_volume)
    except NameError as e:
        print("Bajar volumen ha fallado")

def radiovolup():
    try:
        global vlc_volume
        vlc_volume = vlc_volume+10
        print("Radio Volume: %s ", vlc_volume)
        player.audio_set_volume(vlc_volume)
    except NameError as e:
        print("Subir volumen ha fallado")

def findstream(radiostream):
    streamlist = {
        'pequeradio': 'https://emisorasmusicales.es:8030/pequeradio.mp3',
        'radio one': 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/hls/uk/sbr_high/ak/bbc_radio_one.m3u8',
        'planet rock': 'http://icy-e-bz-08-boh.sharp-stream.com/planetrock.mp3',
        'talk sport': 'http://radio.talksport.com/stream?awparams=platform:ts-tunein;lang:en',
        'talksport': 'http://radio.talksport.com/stream?awparams=platform:ts-tunein;lang:en'
                }
    return streamlist[radiostream]

def radioplay(text):
    print("Emisora seleccionada: %s ", text)
    radiostream = (text.replace('radio', '', 1)).strip()
    print("Volumen: %s ", vlc_volume)
    try:
        stream = findstream(radiostream)
    except KeyError as e:
        logging.error("Error finding stream")
        radiostop()
        return
    print("Reproduciendo radio, emisora: %s ", stream)
    instance = vlc.Instance()
    global player
    player = instance.media_player_new()
    media = instance.media_new(stream)
    player.set_media(media)
    player.audio_set_volume(vlc_volume)
    player.play()

def process_event(assistant, event):
    print(event)
    status_ui = aiy.voicehat.get_status_ui()
    if event.type == EventType.ON_START_FINISHED:
        status_ui.status('ready')
        if sys.stdout.isatty():
            print('Di "OK, Google" y habla, o presiona Ctrl+C para quitar...')
            print('Di "Radio pequeradio"...')

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        status_ui.status('listening')

    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('Has dicho:', event.args['text'])
        text = event.args['text'].lower()
        if text == 'power off':
            assistant.stop_conversation()
            power_off_pi()
        elif 'radio' in text:
            assistant.stop_conversation()
            radioplay(text)
        elif text == 'radio off':
            assistant.stop_conversation()
            radiostop()
        elif text == 'baja el volumen':
            assistant.stop_conversation()
            radiovoldown()
        elif text == 'sube el volumen':
            assistant.stop_conversation()
            radiovolup()    
        elif text == 'reboot':
            assistant.stop_conversation()
            reboot_pi()
        elif text == 'dirección IP':
            assistant.stop_conversation()
            say_ip()

    elif event.type == EventType.ON_END_OF_UTTERANCE:
        status_ui.status('pensando')

    elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
          or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
          or event.type == EventType.ON_NO_RESPONSE):
        status_ui.status('ready')

    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)


def main():
    if platform.machine() == 'armv6l':
        print('Cannot run hotword demo on Pi Zero!')
        exit(-1)

    credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
    with Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(assistant, event)


if __name__ == '__main__':
    main()
