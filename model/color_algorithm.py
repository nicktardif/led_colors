from abc import ABC, abstractmethod
from model.rgb import RGB
import math

class ColorAlgorithm():
    @abstractmethod
    def evaluate(self, ratio: float, led_index: int, led_count: int) -> RGB:
        pass

class RainbowRGB(ColorAlgorithm):
    def __init__(self, offset: float):
        self._offset = offset

    def evaluate(self, ratio: float, _: int, __: int) -> RGB:
        a = math.pi / 2 + (ratio * 2 * math.pi) + self._offset
        r = math.sin(a) * 192 + 128
        g = math.sin(a - (2 * math.pi / 3)) * 192 + 128
        b = math.sin(a - (4 * math.pi / 3)) * 192 + 128
        return RGB(r, g, b)

class RainbowRGBFlow(ColorAlgorithm):
    def __init__(self, offset: float, reverse_leds = False):
        self._offset = offset
        self._reverse_leds = reverse_leds

    def evaluate(self, ratio: float, led_index: int, led_count: int) -> RGB:
        if not self._reverse_leds:
            flow_offset = (2 * math.pi * led_index / led_count)
        else:
            flow_offset = (2 * math.pi * (led_count - led_index) / led_count)
        a = math.pi / 2 + (ratio * 2 * math.pi) + flow_offset + self._offset

        r = math.sin(a) * 192 + 128
        g = math.sin(a - (2 * math.pi / 3)) * 192 + 128
        b = math.sin(a - (4 * math.pi / 3)) * 192 + 128
        return RGB(r, g, b)