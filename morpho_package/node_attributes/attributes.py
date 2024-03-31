from ..point import Point
from ..node import Node
from ..image import Image

class Attributes:

    def __init__(self):
        self.area = None
        self.volume = None
        self.top_left = None
        self.bottom_right = None
        self.height = None
        self.width = None
        self.mean = None
        self.variance = None


    # Pré-ordem
    def preOrderProcess(self, node: Node, image: Image):
        self.area = Area.preOrderArea(node)
        self.volume = Volume.preOrderVolume(node)
        self.top_left, self.bottom_right = Limits.preOrderLimits(node, image)


    # Ordem
    def inOrderProcess(self, image: Image, parent_attribute):
        Area.inOrderArea(parent_attribute, self.area)
        Volume.inOrderVolume(parent_attribute, self.volume)
        Limits.inOrderLimits(parent_attribute, self.top_left, self.bottom_right)


    # Pós-Ordem
    def postOrderProcess(self):
        self.height, self.width = Dimensions.postOrderDimensions(self.top_left, self.bottom_right)


    # Atributos não incrementais
    def nonIncrementalProcess(self, node: Node):
        self.mean = Mean.computeMean(self.volume, self.area)
        self.variance = Variance.computeVariance(node, self.area, self.mean)


    def __str__(self):
        return (
            f"Area: {self.area}\n"
            f"Volume: {self.volume}\n"
            f"Height: {self.height}\n"
            f"Width: {self.width}\n"
            f"TL: {self.top_left}\n"
            f"BR: {self.bottom_right}\n"
            f"Mean: {self.mean}\n"
            f"Variance: {self.variance}"
        )


class Area:

    @staticmethod
    def preOrderArea(node):
        return len(node.cnps)


    @staticmethod
    def inOrderArea(parent_attribute, area):
        parent_attribute.area += area


class Volume:

    @staticmethod
    def preOrderVolume(node):
        return len(node.cnps) * node.level


    @staticmethod
    def inOrderVolume(parent_attribute, volume):
        parent_attribute.volume += volume


class Limits:

    @staticmethod
    def setTopLeft(pixel1: Point, pixel2: Point):
        return Point(
            pixel1.row if pixel1.row < pixel2.row else pixel2.row,
            pixel1.col if pixel1.col < pixel2.col else pixel2.col
        )


    @staticmethod
    def setBottomRight(pixel1: Point, pixel2: Point):
        return Point(
            pixel1.row if pixel1.row > pixel2.row else pixel2.row,
            pixel1.col if pixel1.col > pixel2.col else pixel2.col
        )


    # Pré-Ordem
    @staticmethod
    def preOrderLimits(node: Node, image: Image):
        top_left = image.indexToCoord(node.rep)
        bottom_right = image.indexToCoord(node.rep)
        
        for p in node.cnps:
            pixel = image.indexToCoord(p)
            top_left = Limits.setTopLeft(top_left, pixel)
            bottom_right = Limits.setBottomRight(bottom_right, pixel)
            
        return (top_left, bottom_right)


    # Ordem
    @staticmethod
    def inOrderLimits(parent_attributes: Attributes, top_left: Point, bottom_right: Point):
        parent_attributes.top_left = Limits.setTopLeft(parent_attributes.top_left, top_left)
        parent_attributes.bottom_right = Limits.setBottomRight(parent_attributes.bottom_right, bottom_right)


class Dimensions:

    # Pós-Ordem
    @staticmethod
    def postOrderDimensions(top_left: Point, bottom_right: Point):
        height = Dimensions.postOrderHeight(top_left, bottom_right)
        width = Dimensions.postOrderWidth(top_left, bottom_right)
        return (height, width)


    @staticmethod
    def postOrderHeight(top_left: Point, bottom_right: Point):
        return bottom_right.row - top_left.row + 1


    @staticmethod
    def postOrderWidth(top_left: Point, bottom_right: Point):
        return bottom_right.col - top_left.col + 1


class Mean:

    @staticmethod
    def computeMean(volume: int, area: int) -> float:
        return volume / area


class Variance:

    @staticmethod
    def computeVariance(node: Node, area: int, mean: float) -> float:
        aux = 0
        queue = [node]

        while len(queue) != 0:
            node = queue.pop(0)
            for _ in node.cnps:
                aux += (node.level - mean) ** 2

            queue += node.children

        return aux / area
