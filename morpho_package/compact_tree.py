import numpy as np
import matplotlib.pyplot as plt
from PrettyPrint import PrettyPrintTree

from .adjacency import Adjacency4
from .component_tree import ComponentTree, UpperLevelSets, LowerLevelSets
from .node import Node
from .node_attributes import ComputeAttributes

class CompactTree(ComponentTree):

    def __init__(self, f, adjacency):
        super().__init__(f, adjacency)
        self.computeTree()
        self.canonize()
        ComputeAttributes(self.nodes)


    def canonize(self):
        self.nodes = {}

        for p in np.flip(self.sorted_pixels):
            p_parent = self.parent[p]
            p_grand_parent = self.parent[p_parent]

            p_point = self.pixel_indexer.indexToCoord(p)
            p_parent_point = self.pixel_indexer.indexToCoord(p_parent)
            p_grand_parent_point = self.pixel_indexer.indexToCoord(p_grand_parent)

            if self.image[p_grand_parent_point.row, p_grand_parent_point.col] == self.image[p_parent_point.row, p_parent_point.col]:
                p_parent = self.parent[p] = p_grand_parent

            if p == p_parent or self.image[p_point.row, p_point.col] != self.image[p_parent_point.row, p_parent_point.col]:
                self.generateNode(p)
            else:
                self.nodes[p_parent].addCnp(p)


    def generateNode(self, canonical_index):
        c_point = self.pixel_indexer.indexToCoord(canonical_index)
        level = self.image[c_point.row, c_point.col]
        parent = self.parent[canonical_index]

        if canonical_index == parent:
            self.nodes[canonical_index] = Node(level, canonical_index)
        else:
            self.nodes[canonical_index] = Node(level, canonical_index, self.nodes[parent])
            self.nodes[parent].addChildren(self.nodes[canonical_index])


    def displayTree(self):
        root_index = list(self.nodes.keys())[0]
        root_node = self.nodes[root_index]

        pretty_tree = PrettyPrintTree(
            lambda node: node.childrens.values(),
            lambda node: node.getInfo()
        )
        pretty_tree(root_node)


class MaxTree(CompactTree, UpperLevelSets):
    pass


class MinTree(CompactTree, LowerLevelSets):
    pass
