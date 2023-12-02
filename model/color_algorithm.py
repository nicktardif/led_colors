import math
from abc import ABC, abstractmethod
from hashlib import sha256

from model.color_memo import ColorMemo
from model.rgb import RGB

RGB_SCALAR: int = 192
RGB_OFFSET: int = 128


def hash(val: str) -> str:
    return sha256(val.encode("utf-8")).hexdigest()


class ColorAlgorithm(ABC):
    lookup_key: str
    num_buckets: int
    scale: float
    reverse: bool

    @abstractmethod
    def evaluate(self, percent: float) -> RGB:
        pass

    def is_reverse(self) -> bool:
        return self.reverse

    def get_bucket(self, percent: float) -> int:
        return math.floor(percent * self.num_buckets)


class RainbowRGB(ColorAlgorithm):
    def __init__(
        self,
        offset: float,
        color_memo: ColorMemo,
        scale: float = 1.0,
        reverse: bool = False,
    ):
        self._offset = offset
        self._memo = color_memo
        self.num_buckets = 50
        self.scale = scale
        self.reverse = reverse
        self.lookup_key = hash(self.__class__.__name__ + f"sc_{self.scale}")

    def evaluate(self, percent: float) -> RGB:
        offset_percent = (percent + self._offset) % 1.0
        bucket = self.get_bucket(offset_percent)
        precomputed = self._memo.get(self.lookup_key, bucket)
        if precomputed:
            return precomputed

        a = offset_percent * 2 * math.pi
        r = math.sin(a) * RGB_SCALAR + RGB_OFFSET
        g = math.sin(a - (2 * math.pi / 3)) * RGB_SCALAR + RGB_OFFSET
        b = math.sin(a - (4 * math.pi / 3)) * RGB_SCALAR + RGB_OFFSET

        rgb = RGB(r, g, b)
        self._memo.set_value(self.lookup_key, bucket, rgb)
        return rgb


class Comet(ColorAlgorithm):
    def __init__(
        self,
        offset: float,
        color_memo: ColorMemo,
        scale: float = 1.0,
        reverse: bool = False,
        color_offset: float = 0.0,
    ):
        self._offset = offset
        self._memo = color_memo
        self.num_buckets = 200
        self.scale = scale
        self.reverse = reverse
        self._color_offset = color_offset
        self.lookup_key = hash(
            self.__class__.__name__
            + f"sc_{self.scale}"
            + f"co_{str(self._color_offset)}"
        )

    def evaluate(self, percent: float) -> RGB:
        offset_percent = (percent + self._offset) % 1.0
        bucket = self.get_bucket(offset_percent)
        precomputed = self._memo.get(self.lookup_key, bucket)
        if precomputed:
            return precomputed

        dot_count = 3
        count_per_grouping = self.num_buckets / dot_count
        dropoff_factor = 1 / (count_per_grouping * 2 / 3)
        mod = bucket % (self.num_buckets / dot_count)
        intensity = max(1 - (mod * dropoff_factor), 0)

        a = offset_percent * 2 * math.pi + self._color_offset
        r = intensity * (math.sin(a) * RGB_SCALAR + RGB_OFFSET)
        g = intensity * (math.sin(a - (2 * math.pi / 3)) * RGB_SCALAR + RGB_OFFSET)
        b = intensity * (math.sin(a - (4 * math.pi / 3)) * RGB_SCALAR + RGB_OFFSET)

        rgb = RGB(r, g, b)
        self._memo.set_value(self.lookup_key, bucket, rgb)
        return rgb


class PurpleGreenOrangeComet(Comet):
    def __init__(
        self,
        offset: float,
        color_memo: ColorMemo,
        scale: float = 1.0,
        reverse: bool = False,
    ):
        pgo_color_offset = 2 * math.pi / 3
        super().__init__(offset, color_memo, scale, reverse, pgo_color_offset)


class PastelRGB(ColorAlgorithm):
    def __init__(
        self,
        offset: float,
        color_memo: ColorMemo,
        red_scalar: float = 110,
        red_offset: float = 145,
        green_scalar: float = 110,
        green_offset: float = 145,
        blue_scalar: float = 110,
        blue_offset: float = 145,
        scale: float = 1.0,
        reverse=False,
    ):
        self._offset = offset
        self._memo = color_memo
        self._red_scalar = red_scalar
        self._red_offset = red_offset
        self._green_scalar = green_scalar
        self._green_offset = green_offset
        self._blue_scalar = blue_scalar
        self._blue_offset = blue_offset
        self.scale = scale
        self.lookup_key = hash(
            self.__class__.__name__
            + f"rs_{red_scalar}"
            + f"ro_{red_offset}"
            + f"gs_{green_scalar}"
            + f"go_{green_offset}"
            + f"bs_{blue_scalar}"
            + f"bo_{blue_offset}"
            + f"sc_{self.scale}"
        )
        self.num_buckets = 50
        self.reverse = reverse

    def evaluate(self, percent: float) -> RGB:
        offset_percent = (percent + self._offset) % 1.0
        bucket = self.get_bucket(offset_percent)
        precomputed = self._memo.get(self.lookup_key, bucket)
        if precomputed:
            return precomputed

        a = offset_percent * 2 * math.pi
        r = self._red_scalar * (math.sin(a) + 1) + self._red_offset
        g = self._green_scalar * (math.sin(a - (2 * math.pi / 3))) + self._green_offset
        b = self._blue_scalar * (math.sin(a - (4 * math.pi / 3))) + self._blue_offset

        rgb = RGB(r, g, b)
        self._memo.set_value(self.lookup_key, bucket, rgb)
        return rgb
