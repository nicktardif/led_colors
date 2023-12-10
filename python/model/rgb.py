def _clamp(val):
    return max(0, min(val, 255))


class RGB:
    r: int
    g: int
    b: int

    def __init__(self, r: int, g: int, b: int):
        self.r = _clamp(int(r))
        self.g = _clamp(int(g))
        self.b = _clamp(int(b))

    def __str__(self):
        return f"({self.r}, {self.g}, {self.b})"
