from tkinter import Canvas, Tk
import math
from model.color_algorithm import ColorAlgorithm
from model.point2d import Point2D
from model.rgb import RGB
from model.color_algorithm import RainbowRGB, RainbowRGBReverse
from model.color_memo import ColorMemo
from typing import List, Optional, Any
from time import time_ns

RADIUS = 2
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 700
X_DISTANCE = 6
Y_DISTANCE = 6
LEG_LED_COUNT = 50
TORSO_LED_COUNT = 30
HEAD_LED_COUNT = 50
HEAD_RADIUS = 60
ARM_LED_COUNT = 40
REFRESH_HZ = 30

def _hex_color(rgb: RGB) -> str:
    return "#{0:02x}{1:02x}{2:02x}".format(rgb.r, rgb.g, rgb.b)

def time_ms() -> int:
    return int(time_ns() / 1000000)

class LED():
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

    def _create_circle(self, center: Point2D, r: int, g: int, b: int, canvas: Canvas) -> int:
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

class LEDStrip():
    length: int
    _leds = List[LED]
    _color_algorithm = ColorAlgorithm

    def __init__(self, color_algorithm: ColorAlgorithm):
        self.length = 0
        self._leds = []
        self._color_algorithm = color_algorithm

    def add_led(self, led: LED):
        self.length += 1
        self._leds.append(led)

    def update(self, ratio: float):
        """
        Render the LEDs in the strip according to the color algorithm
        """
        # Signed length supports reversing LED order
        signed_length = self.length if self._color_algorithm.is_reverse() else -1 * self.length

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

def _make_right_leg(canvas: Canvas, leg_root: Point2D, color_algorithm: ColorAlgorithm) -> LEDStrip:
    led_strip = LEDStrip(color_algorithm)
    for i in range(0, LEG_LED_COUNT):
        x = leg_root.x + 1 * i
        y = leg_root.y + Y_DISTANCE * i
        led_strip.add_led(LED(x, y, 255, 0, 255, canvas))
    return led_strip

def _make_left_leg(canvas: Canvas, leg_root: Point2D, color_algorithm: ColorAlgorithm) -> LEDStrip:
    led_strip = LEDStrip(color_algorithm)
    for i in range(0, LEG_LED_COUNT):
        x = leg_root.x - 1 * i
        y = leg_root.y + Y_DISTANCE * i
        led_strip.add_led(LED(x, y, 128, 0, 128, canvas))
    return led_strip

def _make_torso(canvas: Canvas, leg_root: Point2D, color_algorithm: ColorAlgorithm) -> LEDStrip:
    led_strip = LEDStrip(color_algorithm)
    for i in range(0, TORSO_LED_COUNT):
        x = leg_root.x
        y = leg_root.y - Y_DISTANCE * i
        led_strip.add_led(LED(x, y, 128, 0, 128, canvas))
    return led_strip

def _make_head(canvas: Canvas, torso_top: Point2D, color_algorithm: ColorAlgorithm) -> LEDStrip:
    led_strip = LEDStrip(color_algorithm)
    head_center = torso_top + Point2D(0, -1 * HEAD_RADIUS)

    for i in range(0, HEAD_LED_COUNT):
        angle = (360 / HEAD_LED_COUNT) * i
        radians = 2 * math.pi * angle / 360

        x = head_center.x + (math.cos(radians) * HEAD_RADIUS)
        y = head_center.y + (math.sin(radians) * HEAD_RADIUS)
        led_strip.add_led(LED(x, y, 0, 128, 128, canvas))
    return led_strip

def _make_right_arm(canvas: Canvas, arm_root: Point2D, color_algorithm: ColorAlgorithm) -> LEDStrip:
    led_strip = LEDStrip(color_algorithm)
    for i in range(0, ARM_LED_COUNT):
        x = arm_root.x + X_DISTANCE * i
        y = arm_root.y - 2 * i
        led_strip.add_led(LED(x, y, 128, 0, 128, canvas))
    return led_strip

def _make_left_arm(canvas: Canvas, arm_root: Point2D, color_algorithm: ColorAlgorithm) -> LEDStrip:
    led_strip = LEDStrip(color_algorithm)
    for i in range(0, ARM_LED_COUNT):
        x = arm_root.x - X_DISTANCE * i
        y = arm_root.y - 2 * i
        led_strip.add_led(LED(x, y, 128, 0, 128, canvas))
    return led_strip


def main():
    def update_leds():
        time_diff = time_ms() - start_time_ms
        LOOP_TIME_MS = 2000
        percent_through_loop = (time_diff % LOOP_TIME_MS) / LOOP_TIME_MS

        right_leg.update(percent_through_loop)
        left_leg.update(percent_through_loop)
        torso.update(percent_through_loop)
        head.update(percent_through_loop)
        left_arm.update(percent_through_loop)
        right_arm.update(percent_through_loop)

        my_canvas.itemconfig(ratio_text, text=f'Percent: {round(percent_through_loop * 100, 1)}%')

        root.after(int(1000 / REFRESH_HZ), update_leds)

    root = Tk()
    root.geometry(f'{CANVAS_WIDTH}x{CANVAS_HEIGHT}+100+100')
    my_canvas = Canvas(root, bg='black', width=CANVAS_WIDTH, height=CANVAS_HEIGHT)

    # GUI keypoints
    leg_root = Point2D(CANVAS_WIDTH / 2, CANVAS_HEIGHT * 0.55)
    torso_top = Point2D(leg_root.x, leg_root.y - TORSO_LED_COUNT * 6)
    arm_root = torso_top + (leg_root - torso_top) * 0.3

    # Add a memo pad for precomputed color result lookup
    color_memo = ColorMemo()

    # Coloring algorithms
    rainbow_algorithm = RainbowRGB(0, color_memo)
    rainbow_algorithm_arms = RainbowRGBReverse(2/3, color_memo)
    rainbow_algorithm_torso = RainbowRGBReverse(0, color_memo)

    # Make LED strips in a person-shape
    right_leg = _make_right_leg(my_canvas, leg_root, rainbow_algorithm)
    left_leg = _make_left_leg(my_canvas, leg_root, rainbow_algorithm)
    torso = _make_torso(my_canvas, leg_root, rainbow_algorithm_torso)
    head = _make_head(my_canvas, torso_top, rainbow_algorithm)
    right_arm = _make_right_arm(my_canvas, arm_root, rainbow_algorithm_arms)
    left_arm = _make_left_arm(my_canvas, arm_root, rainbow_algorithm_arms)

    ratio_text = my_canvas.create_text(50, 10, text='Ratio: 0%', fill='white')

    start_time_ms = time_ms()
    my_canvas.pack()
    update_leds()

    root.mainloop()

if __name__ == "__main__":
    main()