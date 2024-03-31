from ..compact_tree import CompactTree
from ..node_attributes import Attributes


class Pruning:

    # pruning-min: É uma filtragem onde PODAMOS os nós que atendem um determinado critério
    # e todos os seus descendentes (Entendo que é o que já está feito acima)
    @staticmethod
    def minRule(compact_tree: CompactTree, attributes: Attributes, criteria):
        pruned_image = compact_tree.image.image.flatten().copy()
        stack = [compact_tree.root]

        while len(stack) != 0:
            node = stack.pop()
            attr = attributes[node.index]

            if criteria(attr):
                stack_aux = [node]

                while len(stack_aux) != 0:
                    node_aux = stack_aux.pop()
                    pruned_image[node_aux.cnps] = node.parent.level

                    stack_aux += node_aux.children

            else:
                stack += node.children

        return pruned_image.reshape(compact_tree.image.image.shape)


    # pruning-max: É uma filtragem onde PODAMOS os nós e seus descendentes,
    # somente se TODOS atenderem um determinado critério (Implementar)
    @staticmethod
    def maxRule(compact_tree: CompactTree, attributes: Attributes, criteria):
        pruned_image = compact_tree.image.image.flatten().copy()
        stack = [compact_tree.root]

        while len(stack) != 0:
            node = stack.pop()
            node_attr = attributes[node.index]
            indexes = []

            if criteria(node_attr):
                indexes = [node.rep]

            else:
                while node.parent.index in indexes:
                    indexes.remove(node.parent.index)
                    node = node.parent

            stack += node.children

        for i in indexes:
            node = compact_tree.index_to_node[i]
            new_parent_node = node.parent

            while new_parent_node.index in indexes:
                new_parent_node = new_parent_node.parent

            pruned_image[node.cnps] = new_parent_node.level

        return pruned_image.reshape(compact_tree.image.image.shape)
