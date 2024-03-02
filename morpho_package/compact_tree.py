import numpy as np
import matplotlib.pyplot as plt

from .adjacency import Adjacency4
from .component_tree import ComponentTree, UpperLevelSets, LowerLevelSets
from .node import Node

class CompactTree(ComponentTree):

    def __init__(self, f, adjacency=Adjacency4()):
        super().__init__(f, adjacency)
        self.computeTree()
        self.canonize()


    def canonize(self):
        self.nodes = {}
        self.canonical_pixels = []

        for p in np.flip(self.sorted_pixels):
            p_parent = self.parent[p]
            p_grand_parent = self.parent[p_parent]

            p_point = self.pixel_indexer.index_to_coord(p)
            p_parent_point = self.pixel_indexer.index_to_coord(p_parent)
            p_grand_parent_point = self.pixel_indexer.index_to_coord(p_grand_parent)

            if self.image[p_grand_parent_point.row, p_grand_parent_point.col] == self.image[p_parent_point.row, p_parent_point.col]:
                self.parent[p] = p_grand_parent

            if p == p_parent or self.image[p_point.row, p_point.col] != self.image[p_parent_point.row, p_parent_point.col]:
                self.canonical_pixels.append(p)


class MaxTree(CompactTree, UpperLevelSets):
    pass


class MinTree(CompactTree, LowerLevelSets):
    pass
