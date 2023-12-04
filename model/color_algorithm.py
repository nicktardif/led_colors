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
    def evaluate(self, percent: float, idx: int, total_leds: int) -> RGB:
        pass

    @abstractmethod
    def is_linear(self) -> bool:
        # Return if the color algorithm can be represented as a 1D array, purely linear motion
        pass

    def is_reverse(self) -> bool:
        return self.reverse

    def get_bucket(self, percent: float) -> int:
        return math.floor(percent * self.num_buckets)

    def set_adjustment_level(self, level: int) -> None:
        pass


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
        self.lookup_key = self._calculate_lookup_key()

    def _calculate_lookup_key(self) -> str:
        return hash(self.__class__.__name__ + f"sc_{self.scale}")

    def evaluate(self, percent: float, _: int, __: int) -> RGB:
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

    def is_linear(self):
        return True


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
        self.adjustment_level = 0
        self.lookup_key = self._calculate_lookup_key()

    def _calculate_lookup_key(self) -> str:
        return hash(
            self.__class__.__name__
            + f"sc_{self.scale}"
            + f"co_{str(self._color_offset)}"
            + f"al_{str(self.adjustment_level)}"
        )

    def set_adjustment_level(self, level: int) -> None:
        self.adjustment_level = level
        self.lookup_key = self._calculate_lookup_key()

    def evaluate(self, percent: float, _: int, __: int) -> RGB:
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

        a = (
            offset_percent * 2 * math.pi
            + self._color_offset
            + (self.adjustment_level / 30.0)
        )
        r = intensity * (math.sin(a) * RGB_SCALAR + RGB_OFFSET)
        g = intensity * (math.sin(a - (2 * math.pi / 3)) * RGB_SCALAR + RGB_OFFSET)
        b = intensity * (math.sin(a - (4 * math.pi / 3)) * RGB_SCALAR + RGB_OFFSET)

        rgb = RGB(r, g, b)
        self._memo.set_value(self.lookup_key, bucket, rgb)
        return rgb

    def is_linear(self):
        return True


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

    def evaluate(self, percent: float, _: int, __: int) -> RGB:
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

    def is_linear(self):
        return True


class Yoyo(ColorAlgorithm):
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
        self.adjustment_level = 0
        self.lookup_key = self._calculate_lookup_key()

    def _calculate_lookup_key(self) -> str:
        return hash(
            self.__class__.__name__
            + f"sc_{self.scale}"
            + f"co_{str(self._color_offset)}"
            + f"al_{str(self.adjustment_level)}"
        )

    def set_adjustment_level(self, level: int) -> None:
        self.adjustment_level = level
        self.lookup_key = self._calculate_lookup_key()

    def evaluate(self, percent: float, idx: int, total_count: int) -> RGB:
        # 2.0 is for the yoyo effect
        original_offset_percent = percent + self._offset
        offset_percent = abs((2 * original_offset_percent) % 2.0)
        reverse = False
        if offset_percent >= 1.0:
            offset_percent = 2 - offset_percent
            reverse = True

        bucket = self.get_bucket(original_offset_percent)
        full_key = f"{idx}_{bucket}"
        precomputed = self._memo.get(self.lookup_key, full_key)
        if precomputed:
            return precomputed

        # less dropoff in the middle
        tail_length_percent = math.sin(offset_percent * math.pi) / 4.0
        tail_length_count = tail_length_percent * total_count

        intensity = 0
        if reverse:
            head_idx = math.floor(offset_percent * total_count)
            if head_idx + tail_length_count >= idx and idx >= head_idx:
                intensity = 1
        else:
            head_idx = math.floor(offset_percent * total_count)
            if head_idx - tail_length_count <= idx and idx <= head_idx:
                intensity = 1

        # for each bucket, use the tail length to determine if the specific idx should be displayed
        # dropoff_factor = 1 / (count_per_grouping * diff)

        # intensity = max(1 - (bucket * dropoff_factor), 0)
        # intensity = diff

        # white
        r = intensity * 255
        g = intensity * 255
        b = intensity * 255

        # highlight head in red
        # if idx == head_idx:
        #     r = 255
        #     g = 0
        #     b = 0
        #     # print(
        #     #     f"offset_percent: {round(offset_percent, 2)}, tail_length_percent: {round(tail_length_percent, 2)}, tail length count: {round(tail_length_count, 2)}"
        #     # )

        rgb = RGB(r, g, b)
        self._memo.set_value(self.lookup_key, full_key, rgb)
        return rgb

    def is_linear(self):
        return False
