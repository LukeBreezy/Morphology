from .point import Point

# Representa uma região ou imagem
class Box:

    # def __init__(self, f):
    # 	height, width = f.shape[0], f.shape[1]

    # 	self.top_left = Point(0, 0)
    # 	self.bottom_right = Point(height-1, width-1)

    # 	assert (self.top_left.row < self.bottom_right.row), "bottom is above top in the plane"
    # 	assert (self.top_left.col < self.bottom_right.col), "left is at right of 'right' in the plane"

    def __init__(self, top_left: Point, bottom_right: Point):
        assert (top_left.row < bottom_right.row), "bottom is above top in the plane"
        assert (top_left.col < bottom_right.col), "left is at right of 'right' in the plane"

        self.top_left = top_left
        self.bottom_right = bottom_right

    def top(self):
        return self.top_left.row

    def left(self):
        return self.top_left.col

    def bottom(self):
        return self.bottom_right.row

    def right(self):
        return self.bottom_right.col

    def width(self):
        return self.bottom_right.col - self.top_left.col + 1

    def height(self):
        return self.bottom_right.row - self.top_left.row + 1

    def contains(self, point: Point):
        return  self.left() <= point.col <= self.right() and self.top() <= point.row <= self.bottom()
