"""
LED controls for the Elmo costume
"""

try:
    from typing import List
except ImportError:
    # ignore the error on the RP2040
    pass

import adafruit_fancyled.adafruit_fancyled as fancy
import board
import random
import math
import neopixel
import time

from palette import Palette, ColorPoint
from rgb import RGB


FRAMES_PER_SECOND = 30
LOOP_DURATION_SECONDS = 10
TOTAL_FRAME_COUNT = FRAMES_PER_SECOND * LOOP_DURATION_SECONDS
SPEED_MULTIPLIER = 15.0
LED_BRIGHTNESS = 0.2


def get_ring_pixels() -> neopixel.NeoPixel:
    return neopixel.NeoPixel(
        pin=board.D13,
        n=12,
        brightness=LED_BRIGHTNESS,
        auto_write=False,
        # The order is actually GRBW, translated in the pixel writing layer
        pixel_order=neopixel.RGBW,
    )


def get_flex_pixels() -> neopixel.NeoPixel:
    return neopixel.NeoPixel(
        pin=board.D12,
        n=50,
        brightness=LED_BRIGHTNESS,
        auto_write=False,
        # The order is actually BGR, translated in the pixel writing layer
        pixel_order=neopixel.RGB,
    )

def get_fire_color_map() -> List[RGB]:
    # Compose the fire palette
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

    # Fill out the color map
    color_map: List[RGB] = [None] * TOTAL_FRAME_COUNT
    for i in range(0, TOTAL_FRAME_COUNT):
        percent = i / float(TOTAL_FRAME_COUNT)
        color_map[i] = fire_palette.find_color(percent)
    return color_map


def main():
    ring_pixels = get_ring_pixels()
    flex_pixels = get_flex_pixels()
    color_map = get_fire_color_map()

    current_percent = 0
    target_percent = max(random.random() / 4.0 + 0.75, 1.0)
    speed = random.random() / SPEED_MULTIPLIER + 0.01

    while True:
        # Use a ladder algorithm to randomly move up and down the color palette
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

        # Update ring LEDs
        for led_idx in range(len(ring_pixels)):
            ring_pixels[led_idx] = color.as_grbw()

        # Update the flexible LEDs
        for led_idx in range(len(flex_pixels)):
            flex_pixels[led_idx] = color.as_bgr()

        ring_pixels.show()
        flex_pixels.show()
        time.sleep(1.0 / FRAMES_PER_SECOND)


if __name__ == "__main__":
    main()
