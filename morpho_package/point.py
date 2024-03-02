# Representa um ponto / pixel na imagem
class Point:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def __add__(self, q):
        return Point(self.row + q.row, self.col + q.col)

    def __sub__(self, q):
        return Point(self.row - q.row, self.col - q.col)

    def __eq__(self, q) -> bool:
        return self.row == q.row and self.col == self.col

    def __ne__(self, q) -> bool:
        return not (self == q)

    def __str__(self) -> str:
        return "(" + str(self.row) + ", " + str(self.col) + ")"