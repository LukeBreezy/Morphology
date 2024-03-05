from .point import Point
from .box import Box

# Transforma coordenadas em índices e índices em coordenadas
class PixelIndexer:
    def __init__(self, domain: Box):
        self.domain = domain

    def coordToIndex(self, point: Point):
        q = point - self.domain.top_left
        return self.domain.width() * q.row + q.col

    def indexToCoord(self, index):
        q = Point(index // (self.domain.width()), index % (self.domain.width()))
        return q + self.domain.top_left
