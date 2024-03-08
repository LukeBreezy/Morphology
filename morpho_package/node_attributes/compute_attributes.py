from .attributes import *

class ComputeAttributes:

    def __init__(self, node):
        self.computeIncrementalAttributes(node)


    # Percurso em profundidade (Empilhamento)
    def computeIncrementalAttributes(self, node):
        # Pré-ordem
        node.preOrderProcess()

        for children in node.childrens.values():

            # Ordem
            self.computeIncrementalAttributes(children)
            children.inOrderProcess()
            
        # Pós-ordem
        node.postOrderProcess()

