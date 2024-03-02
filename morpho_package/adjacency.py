from .point import Point

# Representa uma vizinhança com adjacência 4
class Adjacency4:
    def __init__(self):
        self.offsets = [
            Point(row=-1, col=0),
            Point(row=0, col=-1),
            Point(row=0, col=1),
            Point(row=1, col=0),
        ]


    def neighbours(self, point: Point) -> list:
        neighbours = []
        for offset in self.offsets:
            q = offset + point
            neighbours.append(q)
        return neighbours


# Representa uma vizinhança com adjacência 8
class Adjacency8:
    def __init__(self):
        self.offsets = [
            Point(row=-1, col=-1),
            Point(row=-1, col=0),
            Point(row=-1, col=1),
            Point(row=0, col=-1),
            Point(row=0, col=1),
            Point(row=1, col=-1),
            Point(row=1, col=0),
            Point(row=1, col=1)
        ]

    def neighbours(self, point: Point) -> list:
        neighbours = []
        for offset in self.offsets:
            q = offset + point
            neighbours.append(q)
        return neighbours