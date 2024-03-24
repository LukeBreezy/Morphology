import numpy as np


class Pruning:

    def __init__(self, compact_tree, attributes, criteria):
        self.criteria = criteria
        self.pruned_image = compact_tree.image.image.flatten().copy()
        self.prune(compact_tree, attributes, criteria)
        self.pruned_image = self.pruned_image.reshape(compact_tree.image.image.shape)
        

    def prune(self, compact_tree, attributes, criteria):
        stack = [compact_tree.root]

        while len(stack) != 0:
            node = stack.pop()
            attr = attributes[node.index]

            if criteria(attr):
                stack_aux = [node]

                while len(stack_aux) != 0:
                    node_aux = stack_aux.pop()
                    self.pruned_image[node_aux.cnps] = node.parent.level

                    stack_aux += node_aux.children

            else:
                self.pruned_image[node.cnps] = node.level
                stack += node.children