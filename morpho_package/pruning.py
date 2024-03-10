import numpy as np


class Pruning:

    def __init__(self, compact_tree, criteria):
        image = compact_tree.image
        index_to_node = compact_tree.index_to_node
        sorted_pixels = compact_tree.sorted_pixels
        parent = compact_tree.union_find.parent

        self.criteria = criteria
        self.pruned_image = image.image.copy()
        self.prune(sorted_pixels, image, parent, index_to_node)


    def prune(self, sorted_pixels, image, parent, index_to_node):
        for p in sorted_pixels:
            p_parent = parent[p]

            if p == p_parent or image.flatten[p] != image.flatten[p_parent]:
                c_index = p

            else:
                c_index = p_parent
            
            if self.criteria(index_to_node[c_index].attributes):
                new_parent = self.findNewParent(c_index, parent, index_to_node)

                p_point = image.indexToCoord(p)
                new_parent_point = image.indexToCoord(new_parent)

                self.pruned_image[p_point.row, p_point.col] = self.pruned_image[new_parent_point.row, new_parent_point.col]


    def findNewParent(self, c_index, parent, index_to_node):
        if not self.criteria(index_to_node[parent[c_index]].attributes):
            return parent[c_index]

        else:
            return self.findNewParent(parent[c_index], parent, index_to_node)
