from tkinter import Canvas
from typing import Any, List, Optional

from model.color_algorithm import ColorAlgorithm
from model.point2d import Point2D
from model.rgb import RGB

RADIUS = 2


def _hex_color(rgb: RGB) -> str:
    return "#{0:02x}{1:02x}{2:02x}".format(rgb.r, rgb.g, rgb.b)


class LED:
    x: float
    y: float
    r: int
    g: int
    b: int
    _tk_id: Any

    def __init__(self, x: float, y: float, r: int, g: int, b: int, canvas: Canvas):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b
        self._canvas = canvas
        self._tk_id = self._create_circle(Point2D(x, y), r, g, b, self._canvas)

    def _create_circle(
        self, center: Point2D, r: int, g: int, b: int, canvas: Canvas
    ) -> int:
        x0 = center.x - RADIUS
        y0 = center.y - RADIUS
        x1 = center.x + RADIUS
        y1 = center.y + RADIUS
        rgb = RGB(r, g, b)

        hex_code = _hex_color(rgb)
        return canvas.create_oval(x0, y0, x1, y1, fill=hex_code, outline=hex_code)

    def update_color(self, rgb: RGB):
        new_hex = _hex_color(rgb)
        self._canvas.itemconfig(self._tk_id, fill=new_hex, outline=new_hex)


class LEDStrip:
    length: int
    _leds = List[LED]
    _color_algorithm = ColorAlgorithm

    def __init__(self):
        self.length = 0
        self._leds = []
        self._color_algorithm = None

    def add_led(self, led: LED):
        self.length += 1
        self._leds.append(led)

    def set_color_algorithm(self, color_algorithm: ColorAlgorithm):
        self._color_algorithm = color_algorithm

    def update(self, ratio: float):
        """
        Render the LEDs in the strip according to the color algorithm
        """
        # Signed length supports reversing LED order
        signed_length = (
            self.length if self._color_algorithm.is_reverse() else -1 * self.length
        )

        for idx, led in enumerate(self.leds):
            percent = ratio + (idx / signed_length)
            rgb = self._color_algorithm.evaluate(percent)
            led.update_color(rgb)

    def update_algorithm(self, algorithm: ColorAlgorithm):
        self._color_algorithm = algorithm

    def at(self, index: int) -> Optional[LED]:
        return self._leds[index]

    @property
    def leds(self) -> List[LED]:
        return self._leds
