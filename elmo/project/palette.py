try:
    from typing import List
except ImportError:
    pass # ignore the error on the microcontroller

from rgb import RGB
from __future__ import annotations


class ColorPoint:
    def __init__(self, point: float, color: RGB):
        self.point = point
        self.color = color


class Palette:
    color_points: List[ColorPoint]

    def __init__(self, color_points: List[ColorPoint]):
        self.color_points = sorted(color_points, key=lambda l: l.point)

    def find_color(self, point: float) -> RGB:
        # assumes at least 2 color points
        first_idx = 0
        p1 = self.color_points[0]
        p2 = self.color_points[1]

        while True:
            if point >= p1.point and point <= p2.point:
                # found the middle
                ratio = (point - p1.point) / (p2.point - p1.point)
                return p1.color.interpolate(p2.color, ratio)
            else:
                first_idx += 1
                p1 = p2
                p2 = self.color_points[first_idx]
