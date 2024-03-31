from ..compact_tree import CompactTree
from ..node_attributes import Attributes


class Removal:

    # direct: É uma filtragem onde REMOVEMOS apenas os nós que atendem um determinado critério,
    # e atribuimos aos seus filhos o próximo ancestral como novo nó pai (avô dos filhos passa a ser o novo pai)
    @staticmethod
    def directRule(compact_tree: CompactTree, attributes: Attributes, criteria):
        pruned_image = compact_tree.image.image.flatten().copy()
        queue = [compact_tree.root]
        representans = []

        while len(queue) != 0:
            node = queue.pop(0)
            node_attr = attributes[node.index]

            if criteria(node_attr):
                representans.append(node.rep)

            queue += node.children

        for rep in representans:
            node = compact_tree.index_to_node[rep]
            new_parent_node = node.parent

            while new_parent_node.rep in representans:
                new_parent_node = new_parent_node.parent

            pruned_image[node.cnps] = new_parent_node.level

        return pruned_image.reshape(compact_tree.image.image.shape)


    # subtractive: É uma filtragem onde REMOVEMOS apenas os nós que atendem um determinado critério,
    # atribuimos aos seus filhos o próximo ancestral como novo nó pai,
    # e ajustamos seu nível de cinza de acordo com um offset
    @staticmethod
    def subtractiveRule(compact_tree: CompactTree, attributes: Attributes, criteria):
        pruned_image = compact_tree.image.image.flatten().copy()
        queue = [compact_tree.root]
        offsets = [0 for _ in range(compact_tree.tree_size)]

        while len(queue) != 0:
            node = queue.pop(0)
            node_attr = attributes[node.index]

            offsets[node.index] = offsets[node.parent.index]

            if criteria(node_attr):
                offsets[node.index] = node.level - node.parent.level

            queue += node.children

        queue = [compact_tree.root]
        while len(queue) != 0:
            node = queue.pop(0)
            node_attr = attributes[node.index]

            if criteria(node_attr):
                pruned_image[node.cnps] = node.parent.level
            else:
                pruned_image[node.cnps] -= offsets[node.index]
            
            queue += node.children

        return pruned_image.reshape(compact_tree.image.image.shape)
