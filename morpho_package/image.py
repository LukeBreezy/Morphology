# from .box import Box
from typing import Any
from .point import Point
from .box import Box
from .pixel_indexer import PixelIndexer


class Image(PixelIndexer):

    def __init__(self, f):
        self.image = f

        self.height = self.image.shape[0]
        self.width = self.image.shape[1]

        super().__init__(Box(Point(0, 0), Point(self.height - 1, self.width - 1)))


    def contains(self, point):
        return self.domain.contains(point)


    # Dunders Methods (Double Underscore Methods)
    def __array__(self):
        return self.image


    def __repr__(self):
        return self.image
    

    def __getitem__(self, key):
        return self.image[key]


    # Properties
    @property
    def shape(self):
        return self.image.shape


    @property
    def flatten(self):
        return self.image.flatten()
