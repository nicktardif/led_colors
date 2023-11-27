import math
from abc import ABC, abstractmethod
from random import randint

from model.color_memo import ColorMemo
from model.rgb import RGB


class ColorAlgorithm(ABC):
    lookup_key: str
    num_buckets: int

    @abstractmethod
    def evaluate(self, percent: float) -> RGB:
        pass

    @abstractmethod
    def is_reverse(self) -> bool:
        pass

    def get_bucket(self, percent: float) -> int:
        return math.floor(percent * self.num_buckets)


class RainbowRGB(ColorAlgorithm):
    def __init__(self, offset: float, color_memo: ColorMemo):
        self._offset = offset
        self._memo = color_memo
        self.lookup_key = "RainbowRGBFlow"
        self.num_buckets = 50

    def evaluate(self, percent: float) -> RGB:
        offset_percent = (percent + self._offset) % 1.0
        bucket = self.get_bucket(offset_percent)
        precomputed = self._memo.get(self.lookup_key, bucket)
        if precomputed:
            return precomputed

        a = offset_percent * 2 * math.pi
        r = math.sin(a) * 192 + 128
        g = math.sin(a - (2 * math.pi / 3)) * 192 + 128
        b = math.sin(a - (4 * math.pi / 3)) * 192 + 128

        rgb = RGB(r, g, b)
        self._memo.set_value(self.lookup_key, bucket, rgb)
        return rgb

    def is_reverse(self) -> bool:
        return False


class RainbowRGBReverse(RainbowRGB):
    def __init__(self, offset: float, color_memo: ColorMemo):
        super().__init__(offset, color_memo)

    def is_reverse(self) -> bool:
        return True


class PurpleGreenOrangeComet(ColorAlgorithm):
    def __init__(self, offset: float, color_memo: ColorMemo):
        self._offset = offset
        self._memo = color_memo
        self.lookup_key = "PurpleGreenOrangeComet"
        self.num_buckets = 200

    def evaluate(self, percent: float) -> RGB:
        offset_percent = (percent + self._offset) % 1.0
        bucket = self.get_bucket(offset_percent)
        precomputed = self._memo.get(self.lookup_key, bucket)
        if precomputed:
            return precomputed

        dot_count = 3
        mod = bucket % (self.num_buckets / dot_count)
        count_per_grouping = self.num_buckets / dot_count
        mid = count_per_grouping / 2
        intensity = max(
            255 - (1.5 * abs(mod - mid) * (255 / (count_per_grouping / 2))), 0
        )

        a = offset_percent * 2 * math.pi + (math.pi / 3)
        r = intensity * (math.sin(a) * 192 + 128) / 255
        g = intensity * (math.sin(a - (2 * math.pi / 3)) * 192 + 128) / 255
        b = intensity * (math.sin(a - (4 * math.pi / 3)) * 192 + 128) / 255

        rgb = RGB(r, g, b)
        self._memo.set_value(self.lookup_key, bucket, rgb)
        return rgb

    def is_reverse(self) -> bool:
        return False


class PurpleGreenOrangeCometReverse(PurpleGreenOrangeComet):
    def __init__(self, offset: float, color_memo: ColorMemo):
        super().__init__(offset, color_memo)

    def is_reverse(self) -> bool:
        return True
