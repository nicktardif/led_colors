class RGB:
    """
    RGB colors class
    """

    r: int
    g: int
    b: int

    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    def interpolate(self, other: RGB, ratio: float) -> RGB:
        r_diff = other.r - self.r
        g_diff = other.g - self.g
        b_diff = other.b - self.b

        r = int(self.r + (ratio * r_diff))
        g = int(self.g + (ratio * g_diff))
        b = int(self.b + (ratio * b_diff))
        return RGB(r, g, b)

    def as_rgbw(self):
        return (self.r, self.g, self.b, 0)

    def as_grbw(self):
        return (self.g, self.r, self.b, 0)

    def as_bgr(self):
        return (self.b, self.g, self.r)

    def __str__(self):
        return f"({self.r}, {self.g}, {self.b})"
