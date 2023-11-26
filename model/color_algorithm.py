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
        self._count = 0

        self._memo = {}

    def evaluate(self, ratio: float, led_index: int, led_count: int) -> RGB:
        ratio_rounded = round(ratio, 2)
        if self._memo.get(ratio_rounded, {}).get(led_index, None):
            return self._memo.get(ratio_rounded).get(led_index)

        ratio = ratio_rounded
        if not self._reverse_leds:
            flow_offset = (2 * math.pi * led_index / led_count)
        else:
            flow_offset = (2 * math.pi * (led_count - led_index) / led_count)
        a = math.pi / 2 + (ratio * 2 * math.pi) + flow_offset + self._offset

        r = math.sin(a) * 192 + 128
        g = math.sin(a - (2 * math.pi / 3)) * 192 + 128
        b = math.sin(a - (4 * math.pi / 3)) * 192 + 128

        # print computations for memoization evaluation
        self._count +=1
        if self._count % 100 == 0:
            print(self._count)

        rgb = RGB(r, g, b)
        if ratio_rounded not in self._memo:
            self._memo[ratio_rounded] = {led_index: rgb}
        else:
            self._memo[ratio_rounded][led_index] = rgb

        return rgb