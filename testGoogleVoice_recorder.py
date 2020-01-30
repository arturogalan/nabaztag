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

import argparse
import time
import threading

from aiy.board import Board
from aiy.voice.audio import AudioFormat, play_wav, record_file, Recorder

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default='recording.wav')
    args = parser.parse_args()

    with Board() as board:
        print('Press button to start recording.')
        board.button.wait_for_press(timeout=4)

        done = threading.Event()
        board.button.when_pressed = done.set
        board.button.timeout = done.set

        def wait():
            start = time.monotonic()
            duration = time.monotonic() - start

            while duration < 4:
                duration = time.monotonic() - start
                print('Recording: %.02f seconds [Press button to stop]' % duration)
                print(duration < 4)
                time.sleep(0.5)
            

        record_file(AudioFormat.CD, filename=args.filename, wait=wait, filetype='wav')
        print('Press button to play recorded sound.')
        # board.button.wait_for_press(timeout=4)

        print('Playing...')
        play_wav(args.filename)
        print('Done.')

if __name__ == '__main__':
    main()
