from .attributes import *

class ComputeAttributes:

    def __init__(self, compact_tree, attr_list):
        self.computeIncrementalAttributes(compact_tree.root, compact_tree.image, attr_list)


    # Percurso em profundidade (Empilhamento)
    def computeIncrementalAttributes(self, node, image, attr_list):
        attribute_obj = attr_list[node.index]

        # Pré-ordem
        attribute_obj.preOrderProcess(node, image)

        for child in node.children:
            child_attr_obj = attr_list[child.index]

            # Ordem
            self.computeIncrementalAttributes(child, image, attr_list)
            child_attr_obj.inOrderProcess(image, attribute_obj)

        # Pós-ordem
        attribute_obj.postOrderProcess()
