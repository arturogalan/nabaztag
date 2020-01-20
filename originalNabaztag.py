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

'''Signal states on a LED'''

import itertools
import logging
import os
import threading
import time

import RPi.GPIO as GPIO

from neopixel import *
import math
# LED strip configuration:
LED_COUNT      = 32      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0
LED_STRIP      = ws.SK6812_STRIP_GRBW    


logger = logging.getLogger('led')

CONFIG_DIR = os.getenv('XDG_CONFIG_HOME') or os.path.expanduser('~/.config')
CONFIG_FILES = [
    '/etc/status-led.ini',
    os.path.join(CONFIG_DIR, 'status-led.ini')
]


class LED:

    """Starts a background thread to show patterns with the LED."""

    def __init__(self, channel):
        self.animator = threading.Thread(target=self._animate)
        self.channel = channel
        self.iterator = None
        self.running = False
        self.state = None
        self.sleep = 0

        GPIO.setup(channel, GPIO.OUT)
        self.pwm = GPIO.PWM(channel, 100)

        self.iterator_Color = None
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()


    def start(self):
        self.pwm.start(0)  # off by default
        self.running = True

        # Led Ring = CLEAR
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0, 0))
            self.strip.show()

        self.animator.start()

    def stop(self):
        self.running = False
        self.animator.join()
        self.pwm.stop()
        GPIO.output(self.channel, GPIO.LOW)

    def set_state(self, state):
        self.state = state

    def _animate(self):
        # TODO(ensonic): refactor or add justification
        # pylint: disable=too-many-branches
        while self.running:
            if self.state:

                if self.state == 'listening':
                    self.iterator = None
                    self.pwm.ChangeDutyCycle(100)
                    self.sleep = 0.05

                    # Led Ring = ORANGE scrolling
                    ledcolors = []
                    for i in range(self.strip.numPixels()):
                        ledcolors.append(Color(255, 50, 0, 0))
                        for j in range(self.strip.numPixels()-2):
                            ledcolors.append(Color(100, 20, 0, 0))
                    self.iterator_Color = itertools.cycle(ledcolors)

                elif self.state == 'power-off':
                    self.iterator = None
                    self.sleep = 0.0
                    self.pwm.ChangeDutyCycle(0)

                    # Led Ring = CLEAR
                    self.iterator_Color = None
                    for i in range(self.strip.numPixels()):
                        self.strip.setPixelColor(i, Color(0, 0, 0, 0))
                        self.strip.show()

                elif self.state == 'starting':
                    self.iterator = itertools.cycle(
                        itertools.chain(range(0, 100, 10), range(100, 0, -10)))
                    self.sleep = 0.2

                    # Led Ring = WHITE scrolling
                    """Movie theater light style chaser animation."""
                    ledcolors = []
                    for i in range(self.strip.numPixels()):
                        ledcolors.append(Color(0, 0, 0, 100))
                        for j in range(self.strip.numPixels()-2):
                            ledcolors.append(Color(0, 0, 0, 20))
                    self.iterator_Color = itertools.cycle(ledcolors)
                        

                elif self.state == 'thinking':
                    self.iterator = itertools.cycle(
                        itertools.chain(range(0, 100, 5), range(100, 0, -5)))
                    self.sleep = 0.05
                    # Led Ring = GREEN
                    self.iterator_Color = None
                    for i in range(self.strip.numPixels()):
                        self.strip.setPixelColor(i, Color(0, 255, 0, 0))
                        self.strip.show()

                elif self.state == 'stopping':
                    self.iterator = itertools.cycle(
                        itertools.chain(range(0, 100, 5), range(100, 0, -5)))
                    self.sleep = 0.05

                    # Led Ring = WHITE
                    self.iterator_Color = None
                    for i in range(self.strip.numPixels()):
                        self.strip.setPixelColor(i, Color(0, 0, 0, 0))
                        self.strip.show()

                elif self.state == 'ready':
                    self.iterator = itertools.cycle(
                        itertools.chain([0] * 300, range(0, 30, 1), range(30, 0, -1))) # 3 times slower
                    self.sleep = 0.01 # 5 times faster (was 0.05)

                    """Rainbow movie theater light style chaser animation."""
                    ledcolors = []
                    for j in range(256):
                        for i in range(self.strip.numPixels()):
                            ledcolors.append(wheel(math.floor(((i * 255 / self.strip.numPixels()) + j)) & 255))
                    self.iterator_Color = itertools.cycle(ledcolors)
                        


                elif self.state == 'error':
                    self.iterator = itertools.cycle([0, 100] * 3 + [0, 0])
                    self.sleep = 0.25

                    """Movie theater light style chaser animation."""
                    ledcolors = []
                    for i in range(self.strip.numPixels()):
                        ledcolors.append(Color(255, 0, 0, 0))
                        for j in range(self.strip.numPixels()-2):
                            ledcolors.append(Color(100, 0, 0, 0))
                    self.iterator_Color = itertools.cycle(ledcolors)
                
                else:
                    logger.warning("unsupported state: %s", self.state)

                self.state = None
            if self.iterator or self.iterator_Color:
                if self.iterator:
                    self.pwm.ChangeDutyCycle(next(self.iterator))
                
                if self.iterator_Color:
                    for i in range(self.strip.numPixels()):
                        self.strip.setPixelColor(i, next(self.iterator_Color))
                    self.strip.show()

                time.sleep(self.sleep)
            else:
                time.sleep(1)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    )

    import configargparse
    parser = configargparse.ArgParser(
        default_config_files=CONFIG_FILES,
        description="Status LED daemon")
    parser.add_argument('-G', '--gpio-pin', default=25, type=int,
                        help='GPIO pin for the LED (default: 25)')
    args = parser.parse_args()

    led = None
    state_map = {
        "starting": "starting",
        "ready":    "ready",
        "listening": "listening",
        "thinking": "thinking",
        "stopping": "stopping",
        "power-off": "power-off",
        "error":    "error",
    }
    try:
        GPIO.setmode(GPIO.BCM)

        led = LED(args.gpio_pin)
        led.start()
        while True:
            try:
                state = input()
                if not state:
                    continue
                if state not in state_map:
                    logger.warning("unsupported state: %s, must be one of: %s",
                                   state, ",".join(state_map.keys()))
                    continue

                led.set_state(state_map[state])
            except EOFError:
                time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        led.stop()
        GPIO.cleanup()

if __name__ == '__main__':
    main()