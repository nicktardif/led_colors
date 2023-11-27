from time import time_ns
from tkinter import Canvas, Tk

from model.body import TORSO_LED_COUNT, Body
from model.body_group import BodyGroup
from model.color_algorithm import (
    PurpleGreenOrangeComet,
    PurpleGreenOrangeCometReverse,
    RainbowRGB,
    RainbowRGBReverse,
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
        self.color_modes = {
            "rainbow_flow": BodyGroup(
                RainbowRGB(0, color_memo),
                RainbowRGBReverse(0, color_memo),
                RainbowRGBReverse(2 / 3, color_memo),
                RainbowRGBReverse(2 / 3, color_memo),
                RainbowRGB(0, color_memo),
                RainbowRGB(0, color_memo),
            ),
            "pgo_comet": BodyGroup(
                PurpleGreenOrangeComet(0, color_memo),
                PurpleGreenOrangeCometReverse(0, color_memo),
                PurpleGreenOrangeCometReverse(2 / 3, color_memo),
                PurpleGreenOrangeCometReverse(2 / 3, color_memo),
                PurpleGreenOrangeComet(0, color_memo),
                PurpleGreenOrangeComet(0, color_memo),
            ),
        }
        self.color_memo = color_memo

        self.color_mode = "pgo_comet"
        self.ratio_text = self.my_canvas.create_text(
            CANVAS_WIDTH / 2, 10, text="Ratio: 0%", fill="white", justify="left"
        )
        self.mode_text = self.my_canvas.create_text(
            CANVAS_WIDTH / 2,
            30,
            text=f"Mode: {self.color_mode}",
            fill="white",
            justify="left",
        )

        self._set_color_mode(self.color_mode)

        self.root.bind("<Right>", lambda e: self.rightKeyPress(e))
        self.root.bind("<Left>", lambda e: self.leftKeyPress(e))
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
        if current_idx == 0:
            new_idx = len(keys) - 1
        else:
            new_idx = current_idx - 1

        color_mode = keys[new_idx]
        self._set_color_mode(color_mode)

    def rightKeyPress(self, _):
        keys = list(self.color_modes.keys())
        current_idx = keys.index(self.color_mode)
        if current_idx + 1 == len(keys):
            new_idx = 0
        else:
            new_idx = current_idx + 1

        color_mode = keys[new_idx]
        self._set_color_mode(color_mode)

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


def main():
    Main()


if __name__ == "__main__":
    main()
