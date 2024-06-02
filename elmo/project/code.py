""" Simple FancyLED example for NeoPixel strip
"""

try:
    from typing import List
except ImportError:
    pass # ignore the error on the microcontroller

import adafruit_fancyled.adafruit_fancyled as fancy
import board
import random
import math
import neopixel
import time

from palette import Palette, ColorPoint
from rgb import RGB


MAX_POWER = 0.12
FRAMES_PER_SECOND = 30
LOOP_DURATION_SECONDS = 10
TOTAL_FRAME_COUNT = FRAMES_PER_SECOND * LOOP_DURATION_SECONDS
SPEED_MULTIPLIER = 10.0


led_pin = board.D13
num_leds = 12

order = neopixel.GRBW

pixels = neopixel.NeoPixel(
    led_pin, num_leds, brightness=0.2, auto_write=False, pixel_order=order
)

color_map: List[RGB] = [None] * TOTAL_FRAME_COUNT


fire_palette = Palette(
    [
        ColorPoint(0.0, RGB(255.0, 126.0, 50.0)),
        ColorPoint(0.2, RGB(255.0, 101.0, 0.0)),
        ColorPoint(0.4, RGB(254.0, 81.0, 13.0)),
        ColorPoint(0.6, RGB(243.0, 60.0, 4.0)),
        ColorPoint(0.8, RGB(218.0, 31.0, 5.0)),
        ColorPoint(1.0, RGB(161.0, 1.0, 0)),
    ]
)


for i in range(0, TOTAL_FRAME_COUNT):
    percent = i / float(TOTAL_FRAME_COUNT)
    rgb = fire_palette.find_color(percent)
    # my_color = fancy.CRGB(rgb.r, rgb.g, rgb.b)
    # gamma_adjusted = fancy.gamma_adjust(my_color, brightness=MAX_POWER)
    color_map[i] = rgb

current_percent = 0
target_percent = max(random.random() / 4.0 + 0.75, 1.0)
speed = random.random() / SPEED_MULTIPLIER + 0.01

while True:
    current_percent += speed
    if speed > 0:
        # going up
        if current_percent >= target_percent:
            target_percent = random.random() / 4.0
            speed = (-1 * random.random() / SPEED_MULTIPLIER) - 0.01
    else:
        # going down
        if current_percent <= target_percent:
            target_percent = max(random.random() / 4.0 + 0.75, 1.0)
            speed = random.random() / SPEED_MULTIPLIER + 0.01

    current_percent = max(current_percent, 0.0)
    current_percent = min(current_percent, 1.0)

    color_idx = min(
        math.floor(current_percent * TOTAL_FRAME_COUNT), TOTAL_FRAME_COUNT - 1
    )
    color = color_map[color_idx]
    print(f"current percent: {current_percent}, idx: {color_idx}, color: {color}")

    for led_idx in range(num_leds):
        pixels[led_idx] = (color.r, color.g, color.b, 0);

    pixels.show()
    time.sleep(1.0 / FRAMES_PER_SECOND)
