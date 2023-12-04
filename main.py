from time import time_ns
from tkinter import Canvas, Tk
from typing import List

from model.body import TORSO_LED_COUNT, Body
from model.body_group import BodyGroup
from model.color_algorithm import (
    ColorAlgorithm,
    PastelRGB,
    PurpleGreenOrangeComet,
    RainbowRGB,
    Yoyo,
)
from model.color_memo import ColorMemo
from model.point2d import Point2D

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 700
REFRESH_HZ = 30


def time_ms() -> int:
    return int(time_ns() / 1000000)


class Main:
    def __init__(self):
        self.root = Tk()
        self.root.geometry(f"{CANVAS_WIDTH}x{CANVAS_HEIGHT}+100+100")
        self.my_canvas = Canvas(
            self.root, bg="black", width=CANVAS_WIDTH, height=CANVAS_HEIGHT
        )

        # GUI
        leg_root = Point2D(CANVAS_WIDTH / 2, CANVAS_HEIGHT * 0.55)
        torso_top = Point2D(leg_root.x, leg_root.y - TORSO_LED_COUNT * 6)
        arm_root = torso_top + (leg_root - torso_top) * 0.3
        self.body = Body(self.my_canvas, leg_root, torso_top, arm_root)

        # Add a memo pad for precomputed color result lookup
        color_memo = ColorMemo()

        # Coloring algorithms
        rainbow_rgb_no_offset = RainbowRGB(0, color_memo)
        rainbow_rgb_arm_reverse = RainbowRGB(2 / 3, color_memo, reverse=True)
        rainbow_rgb_reverse_no_offset = RainbowRGB(0, color_memo, reverse=True)

        rainbow_rgb_scale3 = RainbowRGB(0, color_memo, scale=3.0)
        rainbow_rgb_scale3_reverse = RainbowRGB(0, color_memo, scale=3.0, reverse=True)
        rainbow_rgb_scale3_arm_reverse = RainbowRGB(
            0.2, color_memo, scale=3.0, reverse=True
        )

        pastel_rgb_1_values = []  # default settings
        pastel_rgb_2_values = [50, 105, 110, 145, 80, 145]
        pastel_rgb_3_values = [10, 105, 110, 145, 40, 145]

        def _pastel_body(rgb_config: List[int]) -> List[ColorAlgorithm]:
            """
            Takes a list of pastel config values and outputs the color algorithms for a pastel body
            """
            return [
                PastelRGB(0, color_memo, *rgb_config, scale=1.0),
                PastelRGB(0, color_memo, *rgb_config, scale=3.0, reverse=True),
                PastelRGB(0.2, color_memo, *rgb_config, scale=3.0, reverse=True),
                PastelRGB(0.2, color_memo, *rgb_config, scale=3.0, reverse=True),
                PastelRGB(0, color_memo, *rgb_config, scale=3.0),
                PastelRGB(0, color_memo, *rgb_config, scale=3.0),
            ]

        self.color_modes = {
            "rainbow": BodyGroup(
                rainbow_rgb_no_offset,
                rainbow_rgb_reverse_no_offset,
                rainbow_rgb_arm_reverse,
                rainbow_rgb_arm_reverse,
                rainbow_rgb_no_offset,
                rainbow_rgb_no_offset,
            ),
            "rainbow_long": BodyGroup(
                rainbow_rgb_no_offset,
                rainbow_rgb_scale3_reverse,
                rainbow_rgb_scale3_arm_reverse,
                rainbow_rgb_scale3_arm_reverse,
                rainbow_rgb_scale3,
                rainbow_rgb_scale3,
            ),
            "pastel_rgb": BodyGroup(*_pastel_body(pastel_rgb_1_values)),
            "pastel_rgb_2": BodyGroup(*_pastel_body(pastel_rgb_2_values)),
            "pastel_rgb_3": BodyGroup(*_pastel_body(pastel_rgb_3_values)),
            "pgo_comet": BodyGroup(
                PurpleGreenOrangeComet(0, color_memo),
                PurpleGreenOrangeComet(0, color_memo, reverse=True),
                PurpleGreenOrangeComet(2 / 3, color_memo, reverse=True),
                PurpleGreenOrangeComet(2 / 3, color_memo, reverse=True),
                PurpleGreenOrangeComet(0, color_memo),
                PurpleGreenOrangeComet(0, color_memo),
            ),
            "pgo_comet_in_to_out": BodyGroup(
                PurpleGreenOrangeComet(0, color_memo),
                PurpleGreenOrangeComet(0, color_memo, scale=8),
                PurpleGreenOrangeComet(1 / 4, color_memo, scale=8),
                PurpleGreenOrangeComet(1 / 4, color_memo, scale=8),
                PurpleGreenOrangeComet(3 / 4, color_memo, scale=8),
                PurpleGreenOrangeComet(3 / 4, color_memo, scale=8),
            ),
            "yoyo": BodyGroup(
                Yoyo(0, color_memo),
                Yoyo(0, color_memo),
                Yoyo(0, color_memo),
                Yoyo(0, color_memo),
                Yoyo(0, color_memo),
                Yoyo(0, color_memo),
            ),
        }
        self.color_memo = color_memo

        self.color_mode = "yoyo"
        self.ratio_text = self.my_canvas.create_text(
            CANVAS_WIDTH / 2, 10, text="Ratio: 0%", fill="white", justify="left"
        )
        self.adjustment_level = 0
        self.mode_text = self.my_canvas.create_text(
            CANVAS_WIDTH / 2,
            30,
            text=f"Mode: {self.color_mode}",
            fill="white",
            justify="left",
        )
        self.adjustment_text = self.my_canvas.create_text(
            CANVAS_WIDTH / 2,
            50,
            text=f"Adjustment: {self.adjustment_level}",
            fill="white",
            justify="left",
        )

        self._set_color_mode(self.color_mode)

        self.root.bind("<Right>", lambda e: self.rightKeyPress(e))
        self.root.bind("<Left>", lambda e: self.leftKeyPress(e))
        self.root.bind("<Up>", lambda e: self.upKeyPress(e))
        self.root.bind("<Down>", lambda e: self.downKeyPress(e))
        self.root.bind("<Escape>", lambda e: self.escapeKeyPress(e))

        self.start_time_ms = time_ms()
        self.my_canvas.pack()
        self.update_leds()

        self.root.mainloop()

    def update_leds(self):
        time_diff = time_ms() - self.start_time_ms
        LOOP_TIME_MS = 2000
        percent_through_loop = (time_diff % LOOP_TIME_MS) / LOOP_TIME_MS

        self.body.right_leg.update(percent_through_loop)
        self.body.left_leg.update(percent_through_loop)
        self.body.torso.update(percent_through_loop)
        self.body.head.update(percent_through_loop)
        self.body.left_arm.update(percent_through_loop)
        self.body.right_arm.update(percent_through_loop)

        self.my_canvas.itemconfig(
            self.ratio_text, text=f"Percent: {round(percent_through_loop * 100, 1)}%"
        )

        self.root.after(int(1000 / REFRESH_HZ), self.update_leds)

    def escapeKeyPress(self, _):
        self.root.destroy()

    def leftKeyPress(self, _):
        keys = list(self.color_modes.keys())
        current_idx = keys.index(self.color_mode)
        new_idx = len(keys) - 1 if current_idx == 0 else current_idx - 1

        color_mode = keys[new_idx]
        self._set_color_mode(color_mode)

    def rightKeyPress(self, _):
        keys = list(self.color_modes.keys())
        current_idx = keys.index(self.color_mode)
        new_idx = 0 if current_idx + 1 == len(keys) else current_idx + 1

        color_mode = keys[new_idx]
        self._set_color_mode(color_mode)

    def upKeyPress(self, _):
        self._set_adjustment_level(self.adjustment_level + 1)

    def downKeyPress(self, _):
        self._set_adjustment_level(self.adjustment_level - 1)

    def _set_color_mode(self, color_mode: str):
        self.color_mode = color_mode
        body_group: BodyGroup = self.color_modes[color_mode]

        self.body.head.set_color_algorithm(body_group.head)
        self.body.torso.set_color_algorithm(body_group.torso)
        self.body.right_arm.set_color_algorithm(body_group.right_arm)
        self.body.left_arm.set_color_algorithm(body_group.left_arm)
        self.body.right_leg.set_color_algorithm(body_group.right_leg)
        self.body.left_leg.set_color_algorithm(body_group.left_leg)

        self.my_canvas.itemconfig(self.mode_text, text=f"Mode: {self.color_mode}")

    def _set_adjustment_level(self, adjustment_level: int):
        self.adjustment_level = adjustment_level

        self.body.head._color_algorithm.set_adjustment_level(self.adjustment_level)
        self.body.torso._color_algorithm.set_adjustment_level(self.adjustment_level)
        self.body.right_arm._color_algorithm.set_adjustment_level(self.adjustment_level)
        self.body.left_arm._color_algorithm.set_adjustment_level(self.adjustment_level)
        self.body.right_leg._color_algorithm.set_adjustment_level(self.adjustment_level)
        self.body.left_leg._color_algorithm.set_adjustment_level(self.adjustment_level)

        self.my_canvas.itemconfig(
            self.adjustment_text, text=f"Adjustment: {self.adjustment_level}"
        )


def main():
    Main()


if __name__ == "__main__":
    main()
