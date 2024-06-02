class Point2D:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, val):
        return Point2D(self.x + val.x, self.y + val.y)

    def __sub__(self, val):
        return Point2D(self.x - val.x, self.y - val.y)

    def __mul__(self, val):
        return Point2D(self.x * val, self.y * val)
