from abc import ABC, abstractmethod
from model.rgb import RGB
import math
from model.color_memo import ColorMemo

class ColorAlgorithm(ABC):
    lookup_key: str

    @abstractmethod
    def evaluate(self, percent: float) -> RGB:
        pass

    @abstractmethod
    def is_reverse(self) -> bool:
        pass

class RainbowRGB(ColorAlgorithm):
    def __init__(self, offset: float, color_memo: ColorMemo):
        self._offset = offset
        self._count = 0
        self._memo = color_memo
        self.lookup_key = 'RainbowRGBFlow'

    def evaluate(self, percent: float) -> RGB:
        offset_percent = round((percent + self._offset) % 1.0, 2)
        precomputed = self._memo.get(self.lookup_key, offset_percent)
        if precomputed:
            return precomputed

        a = offset_percent * 2 * math.pi
        r = math.sin(a) * 192 + 128
        g = math.sin(a - (2 * math.pi / 3)) * 192 + 128
        b = math.sin(a - (4 * math.pi / 3)) * 192 + 128

        rgb = RGB(r, g, b)
        self._memo.set_value(self.lookup_key, offset_percent, rgb)
        return rgb

    def is_reverse(self) -> bool:
        return False

class RainbowRGBReverse(RainbowRGB):
    def __init__(self, offset: float, color_memo: ColorMemo):
        super().__init__(offset, color_memo)

    def is_reverse(self) -> bool:
        return True