import math
from tkinter import Canvas

from model.led import LED, LEDStrip
from model.point2d import Point2D

X_DISTANCE = 6
Y_DISTANCE = 6
LEG_LED_COUNT = 50
TORSO_LED_COUNT = 30
HEAD_LED_COUNT = 50
HEAD_RADIUS = 60
ARM_LED_COUNT = 40


class Body:
    head: LEDStrip
    torso: LEDStrip
    left_arm: LEDStrip
    right_arm: LEDStrip
    left_leg: LEDStrip
    right_leg: LEDStrip

    def __init__(
        self, canvas: Canvas, leg_root: Point2D, torso_top: Point2D, arm_root: Point2D
    ):
        self._canvas = canvas
        self._leg_root = leg_root
        self._arm_root = arm_root
        self._torso_top = torso_top

        # Make LED strips in a person-shape
        self.right_leg = self._make_right_leg()
        self.left_leg = self._make_left_leg()
        self.torso = self._make_torso()
        self.head = self._make_head()
        self.right_arm = self._make_right_arm()
        self.left_arm = self._make_left_arm()

    def _make_right_leg(self) -> LEDStrip:
        led_strip = LEDStrip()
        for i in range(0, LEG_LED_COUNT):
            x = self._leg_root.x + 1 * i
            y = self._leg_root.y + Y_DISTANCE * i
            led_strip.add_led(LED(x, y, 255, 0, 255, self._canvas))
        return led_strip

    def _make_left_leg(self) -> LEDStrip:
        led_strip = LEDStrip()
        for i in range(0, LEG_LED_COUNT):
            x = self._leg_root.x - 1 * i
            y = self._leg_root.y + Y_DISTANCE * i
            led_strip.add_led(LED(x, y, 128, 0, 128, self._canvas))
        return led_strip

    def _make_torso(self) -> LEDStrip:
        led_strip = LEDStrip()
        for i in range(0, TORSO_LED_COUNT):
            x = self._leg_root.x
            y = self._leg_root.y - Y_DISTANCE * i
            led_strip.add_led(LED(x, y, 128, 0, 128, self._canvas))
        return led_strip

    def _make_head(self) -> LEDStrip:
        led_strip = LEDStrip()
        head_center = self._torso_top + Point2D(0, -1 * HEAD_RADIUS)

        for i in range(0, HEAD_LED_COUNT):
            angle = (360 / HEAD_LED_COUNT) * i
            radians = 2 * math.pi * angle / 360

            x = head_center.x + (math.cos(radians) * HEAD_RADIUS)
            y = head_center.y + (math.sin(radians) * HEAD_RADIUS)
            led_strip.add_led(LED(x, y, 0, 128, 128, self._canvas))
        return led_strip

    def _make_right_arm(self) -> LEDStrip:
        led_strip = LEDStrip()
        for i in range(0, ARM_LED_COUNT):
            x = self._arm_root.x + X_DISTANCE * i
            y = self._arm_root.y - 2 * i
            led_strip.add_led(LED(x, y, 128, 0, 128, self._canvas))
        return led_strip

    def _make_left_arm(self) -> LEDStrip:
        led_strip = LEDStrip()
        for i in range(0, ARM_LED_COUNT):
            x = self._arm_root.x - X_DISTANCE * i
            y = self._arm_root.y - 2 * i
            led_strip.add_led(LED(x, y, 128, 0, 128, self._canvas))
        return led_strip
