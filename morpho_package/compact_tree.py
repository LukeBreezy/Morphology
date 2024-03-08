import numpy as np
import matplotlib.pyplot as plt
from PrettyPrint import PrettyPrintTree

from .adjacency import Adjacency4
from .component_tree import ComponentTree
from .node import Node
from .node_attributes import ComputeAttributes


class CompactTree(ComponentTree):

    def __init__(self, f, adjacency):
        super().__init__(f, adjacency)

        self.nodes = {}
        self.generateTree()
        ComputeAttributes(self.root)


    def generateTree(self):
        for p in np.flip(self.sorted_pixels):
            p_parent = self.union_find.parent[p]

            p_point = self.image.indexToCoord(p)
            p_parent_point = self.image.indexToCoord(p_parent)

            if p == p_parent:
                self.generateNode(p, True)

            elif self.image[p_point.row, p_point.col] != self.image[p_parent_point.row, p_parent_point.col]:
                self.generateNode(p, False)

            else:
                self.nodes[p_parent].addCnp(p)
                p_point = self.image.indexToCoord(p)
                self.nodes[p_parent].setLimits(p_point)


    def generateNode(self, canonical_index, is_root):
        c_point = self.image.indexToCoord(canonical_index)
        level = self.image[c_point.row, c_point.col]
        c_parent = self.union_find.parent[canonical_index]

        if is_root:
            self.nodes[canonical_index] = self.root = Node(level, canonical_index)

        else:
            self.nodes[canonical_index] = Node(level, canonical_index, self.nodes[c_parent])
            self.nodes[c_parent].addChildren(self.nodes[canonical_index])

        self.nodes[canonical_index].top_left = self.image.indexToCoord(canonical_index)
        self.nodes[canonical_index].bottom_right = self.image.indexToCoord(canonical_index)


    def displayTree(self):
        pretty_tree = PrettyPrintTree(
            lambda node: node.childrens.values(),
            lambda node: node.getInfo()
        )
        pretty_tree(self.root)


class MaxTree(CompactTree):

    def sortPixels(self):
        return super().sortPixels('desc')


class MinTree(CompactTree):

    def sortPixels(self):
        return super().sortPixels('asc')